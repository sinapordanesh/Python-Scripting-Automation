import contextlib
import os
import queue
import requests
import sys
import threading
import time

# list of file extensions that we aren’t interested in
FILTERED = [".jpg", ".gif", ".png", ".css"]
TARGET = "<http://boodelyboo.com/wordpress>"
THREADS = 10

# the Queue object where we’ll put the filepaths we’ve located locally
answers = queue.Queue()
# we’ll store the files that we’ll attempt to locate on the remote server
web_paths = queue.Queue()

"""
to walk down the distribution, inserting each full filepath into a queue
"""
def gather_paths():
    # walk through all of the files and directories in the local web application directory
    for root, _, files in os.walk('.'):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            # each valid file -> add it to the web_paths
            web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
    """
    On enter, change directory to specified path.
    On exit, change directory back to original.
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        # yields control back to gather_paths
        yield
    finally:
        # reverts to the original directory
        os.chdir(this_dir)

if __name__ == '__main__':
    with chdir("/home/tim/Downloads/wordpress"):
        gather_paths()
    input('Press return to continue.')