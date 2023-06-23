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
