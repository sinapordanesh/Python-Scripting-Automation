# `pcap` Processing

We will approach this task from a different perspective by extracting image files from HTTP traffic. Once we have these image files, we will utilize OpenCV (**http://www.opencv.org/**), a computer vision tool, to detect human faces in the images. This will help us filter out and focus on the images that are potentially interesting.

This example focuses on two tasks: extracting images from HTTP traffic and detecting faces within those images. To accomplish this, we have two separate programs: `recapper.py` and `detector.py`.

`Recapper.py` analyzes a pcap file, extracts any images found in the network streams, and saves them to disk.

`Detector.py` processes the saved image files, identifies faces within them, and generates new images with highlighted face regions.

### `recapper.py`

```python
from scapy.all import TCP, rdpcap
import collections
import os
import re
import sys
import zlib

""""
specify the location of the directory in which to output the images and the location of the pcap file to read
"""
OUTDIR = '/root/Desktop/pictures'
PCAPS = '/root/Downloads'

Response = collections.namedtuple('Response', ['header', 'payload'])

""""
The get_header function takes the raw HTTP traffic and spits out the
headers.
"""
def get_header(payload):
    try:
        # extracting the header portion -> finding the index of the double -> slicing the payload accordingly 
        header_raw = payload[:payload.index(b'\\r\\n\\r\\n')+2]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    
    # create a dictionary (header) from the decoded payload -> spliting on the colon
    header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\\r\\n', header_raw.decode()))
    if 'Content-Type' not in header:
        # header doesn’t contain the data we want to extract
        return None
    return header

""""
The extract_content function takes the HTTP response and the name for the content type we want to extract.
"""
def extract_content(response, content_name='image'):

    content, content_type = None, None
    
    if content_name in Response.header['Content-Type']:

        # actual content type specified in the header
        content_type = Response.header['Content-Type'].split('/')[1]

        # hold the content itself
        content = Response.payload[Response.payload.index(b'\\r\\n\\r\\n')+4:]

        # If the content has been encoded
        if 'Content-Encoding' in Response.header:
            # decompress the content by using the zlib module
            if Response.header['Content-Encoding'] == "gzip":
                content = zlib.decompress(Response.payload, zlib.MAX_WBITS | 32)
            elif Response.header['Content-Encoding'] == "deflate":
                content = zlib.decompress(Response.payload)

    # return a tuple of the content and content_type
    return content, content_type

class Recapper:
    # initialize the object
    def __init__(self, fname):
        pcap = rdpcap(fname)

        # feature of Scapy to automatically separate each TCP session
        self.sessions = pcap.sessions()
        # empty list -> fill in with the responses from the pcap file
        self.responses = list()

    """"
    read responses from the pcap file.
    traverse the packets to find each separate Response and add each one to the list of responses present in the packet stream.
    """
    def get_responses(self):
        # iterate over the sessions dictionary
        for session in self.sessions:
            payload = b''
            # iterate over the packets within each session
            for packet in self.sessions[session]:
                try:
                    # only packets with a destination or source port of 80
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:

                        # concatenate the payload of all the traffic into a single buffer
                        payload += bytes(packet[TCP].payload)

                # If we don’t succeed in appending -> print an x to the console & continue
                except IndexError:
                    sys.stdout.write('x')
                    sys.stdout.flush()

            # if the payload byte string is not empty
            if payload:
                # pass it off to the HTTP header-parsing function get_header
                header = get_header(payload)
                if header is None:
                    continue
                # append the Response to the responses list
                self.responses.append(Response(header=header, payload=payload))

    """"
    write image files contained in the responses to the output directory
    """
    def write(self, content_name):
        # iterate over the responses
        for i, response in enumerate(self.responses):
            # extract the content
            content, content_type = extract_content(response, content_name)
            if content and content_type:
                fname = os.path.join(OUTDIR, f'ex_{i}.{content_type}')
                print(f'Writing {fname}')
                with open(fname, 'wb') as f:
                    # write that content to a file
                    f.write(content)

if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_responses()
    recapper.write('image')
```

The code above demonstrates how to extract images from a packet capture (pcap) file using Scapy.

The `Recapper` class is initialized with the pcap file name, and the `get_responses()` method is used to read the responses from the pcap file. The method iterates over the sessions within the pcap file and concatenates the payload of all the traffic into a single buffer. Then, it passes the buffer to the `get_header()` function to extract the HTTP headers. If the headers contain the specified content type, the `extract_content()` method extracts the content and saves it to a file.

The `write()` method writes image files contained in the responses to the output directory. It iterates over the responses and uses the `extract_content()` method to extract the content of the specified content type. If the content exists, it writes the content to a file with the extension specified by the content type.

To use this code, the user must provide the path of the pcap file in the `Recapper` class initialization and specify the content type to extract in the `write()` method.

Overall, this code demonstrates how Scapy can be used to extract images from a pcap file.

### `detector.py`

```python
import cv2
import os

ROOT = '/root/Desktop/pictures'
FACES = '/root/Desktop/faces'
TRAIN = '/root/Desktop/training'

def detect(srcdir=ROOT, tgtdir=FACES, train_dir=TRAIN):
    for fname in os.listdir(srcdir):
        # iterates over the JPG files
        if not fname.upper().endswith('.JPG'):
            continue
        fullname = os.path.join(srcdir, fname)
        newname = os.path.join(tgtdir, fname)
        # read the image by using the OpenCV computer vision library cv2
        img = cv2.imread(fullname)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        training = os.path.join(train_dir, 'haarcascade_frontalface_alt.xml')
        # create the cv2 face detector object
        cascade = cv2.CascadeClassifier(training)
        rects = cascade.detectMultiScale(gray, 1.3, 5)
        try:
            # in which faces are found
            if rects.any():
                print('Got a face')
                # Python slice syntax to convert from one form to another
                rects[:, 2:] += rects[:, :2]
        except AttributeError:
            print(f'No faces found in {fname}.')
            continue
        # highlight the faces in the image
        for x1, y1, x2, y2 in rects:
            # draw a green box around the face
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
        # write the image to the output directory
        cv2.imwrite(newname, img)

if __name__ == '__main__':
    detect()
```

The code above demonstrates how to detect human faces in images using the OpenCV computer vision library.

The `detect()` function takes the path of the source directory (`srcdir`), target directory (`tgtdir`), and training directory (`train_dir`) as input. The function iterates over the JPG files in the source directory and reads each image using the `cv2.imread()` function from OpenCV. If the image is successfully read, the function converts it to grayscale using `cv2.cvtColor()` and creates a face detector object using the `cv2.CascadeClassifier()` function with the Haar Cascade training data file (`haarcascade_frontalface_alt.xml`) stored in the training directory.

The `cv2.CascadeClassifier.detectMultiScale()` function is used to detect faces in the grayscale image. If one or more faces are detected, the function draws a green box around each face using `cv2.rectangle()` and saves the image to the target directory using `cv2.imwrite()`.

To use this code, the user must specify the source directory, target directory, and training directory in the function call.

Overall, this code demonstrates how OpenCV can be used to detect human faces in images.

## **Kicking the Tires (Kali VM)**

- installed the OpenCV libraries:
    
    ```python
    #:> apt-get install libopencv-dev python3-opencv python3-numpy python3-scipy
    ```
    
- grab the facial detection training file:
    
    ```python
    #:> wget http://eclecti.cc/files/2008/03/haarcascade_frontalface_alt.xml
    ```
    
    Copy the downloaded file to the directory we specified in the TRAIN variable in *`detector.py`.*
    
- create a couple of directories for the output, drop in a pcap, and run the scripts:
    
    ```python
    #:> mkdir /root/Desktop/pictures
    #:> mkdir /root/Desktop/faces
    #:> python recapper.py
    ```
    
    ```python
    #:> python detector.py
    ```