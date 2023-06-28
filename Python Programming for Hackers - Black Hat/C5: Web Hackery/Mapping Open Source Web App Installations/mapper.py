import contextlib
import os
import queue
import requests
import sys
import threading
import time

# list of file extensions that we aren’t interested in
FILTERED = [".jpg", ".gif", ".png", ".css"]
TARGET = "<https://tastykitchen.com/wordpress>"
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


""""
Process web paths from the `web_paths` queue by appending them to the `target_website` base path and attempting to retrieve them. If the response code is 200, add the URL to the `answers` queue and print '+' on the console. Otherwise, print 'x' and continue the loop.
"""
def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}'
        time.sleep(2) # your target may have throttling/lockout.
        r = requests.get(url)
        if r.status_code == 200:
            #put succeed URL into the answers queue
            answers.put(url)
            sys.stdout.write('+')
        else:
            sys.stdout.write('x')
        sys.stdout.flush()


""""
The run function orchestrates the mapping process, calling the functions just defined.
"""
def run():
    mythreads = list()
    for i in range(THREADS):
        print(f'Spawning thread {i}')
        # each thread run the test_remote function
        t = threading.Thread(target=test_remote)
        mythreads.append(t)
        t.start()
    for thread in mythreads:
        thread.join()



if __name__ == '__main__':

    # context manager
    with chdir("/home/tim/Downloads/wordpress"):
        gather_paths()

    # review the console output before continuing
    input('Press return to continue.')

    # run the main mapping task
    run()

    # a block to write the results to a file
    with open('myanswers.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\\n')
    print('done')
