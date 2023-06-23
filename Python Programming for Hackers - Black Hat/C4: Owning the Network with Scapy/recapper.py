from scapy.all import TCP, rdpcap
import collections
import os
import re
import sys
import zlib

OUTDIR = '/root/Desktop/pictures'
PCAPS = '/root/Downloads'

Response = collections.namedtuple('Response', ['header', 'payload'])

def get_header(payload):
    pass

def extract_content(response, content_name='image'):
    pass

class Recapper:
    def __init__(self, fname):
        self.fname = fname
        self.packets = rdpcap(self.fname)

    def get_responses(self):
        self.responses = []
        for packet in self.packets:
            if TCP in packet:
                payload = packet[TCP].payload
                if 'Content-Type' in str(payload):
                    header, payload = payload.split(b'\\r\\n\\r\\n', 1)
                    self.responses.append(Response(header, payload))

    def write(self, content_name):
        if not os.path.exists(OUTDIR):
            os.makedirs(OUTDIR)
        for i, response in enumerate(self.responses):
            if content_name in str(response.header):
                content = zlib.decompress(response.payload, 16+zlib.MAX_WBITS)
                fname = os.path.join(OUTDIR, f'{content_name}_{i}.jpg')
                with open(fname, 'wb') as f:
                    f.write(content)

if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_responses()
    recapper.write('image')
