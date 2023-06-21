# Replacing Netcat

## Code

### `netcat.py`

```python
# Copyright (C) 2023 Saman Pordanesh
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files...

import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

class NetCat:
    def __init__(self, args, buffer=None): # initialize the NetCat object with the arguments from the commandline and the buffer
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create the socket object
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self): # run the command line
        #If we’re setting up a listener, we call the listen method. Otherwise, we call the send method
        if self.args.listen:
            self.listen()
        else:
            self.send()

    # program run as a sender   
    def send(self): 
        self.socket.connect((self.args.target, self.args.port)) # connect to the target and port
        if self.buffer: #if we have a buffer, we send that to the target first
            self.socket.send(self.buffer)
        try: # try/catch -> CTRL-C manual closing 
            while True: # loop to receive data from the target.
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096: # if no more data, we break out of the loop
                        break 
                if response: # print the response data
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode()) # get interactive input, send that input
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    # program run as a listener
    def listen(self):
        self.socket.bind((self.args.target, self.args.port)) # listen method binds to the target and port
        self.socket.listen(5)
        while True: # starts listening in a loop
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread( # passing the connected socket to the handle method
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    # logic to perform file uploads, execute commands, and create an interactive shell.        
    def handle(self, client_socket):
        if self.args.execute: # If a command should be executed
            output = execute(self.args.execute) # passes that Basic Networking Tools command to the execute function
            client_socket.send(output.encode()) # sends the output back on the socket

        elif self.args.upload: # If a file should be uploaded
            file_buffer = b''
            while True: # set up a loop to listen for content on the listening socket
                # receive data until there’s no more data
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            # write that accumulated content to the specified file.
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command: # if the shell is to be created
            cmd_buffer = b''
            while True: # loop, send a prompt to the sender, and wait for a command string to come back
                try:
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode()) # execute the command by using the execute function
                    if response:
                        client_socket.send(response.encode()) # return the output of the command to the sender
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return 
    output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT) #1
    return output.decode()

if __name__ == '__main__':
        
    parser = argparse.ArgumentParser( #create a commandline interface from 'argparse' module
    description='BHP Net Tool',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''Example:  
        netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell 
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
        netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd" # execute command
        echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
        netcat.py -t 192.168.1.108 -p 5555 # connect to server
    ''')) #provide example usage when --help
        
    # six arguments for indicating how the program to behave
    parser.add_argument('-c', '--command', action='store_true', help='command shell') # sets up an interactive shell
    parser.add_argument('-e', '--execute', help='execute specified command') # executes one specific command
    parser.add_argument('-l', '--listen', action='store_true', help='listen') # indicates that a listener should be set up,
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port') # specifies the port on which to communicate
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP') # specifies the target IP
    parser.add_argument('-u', '--upload', help='upload file') # specifies the name of a file to upload.
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
        
    nc = NetCat(args, buffer.encode()) # initialize the NetCat
    nc.run(
```

## Explanation

The provided code is an implementation of a simple NetCat tool using Python. NetCat is a versatile networking tool that allows you to read from and write to network connections. It can be used for various purposes such as debugging, port scanning, transferring files, and creating reverse shells.

Here's an explanation of the code:

1. The code begins by importing the required modules (**`argparse`**, **`socket`**, **`shlex`**, **`subprocess`**, **`sys`**, **`textwrap`**, and **`threading`**).
2. The **`NetCat`** class is defined, which serves as the main component of the NetCat tool. It has methods for sending and receiving data over a network connection.
3. The **`__init__`** method initializes the **`NetCat`** object. It takes **`args`** (parsed command-line arguments) and **`buffer`** (input data) as parameters. It sets up a socket object, configures it, and stores the arguments and buffer.
4. The **`run`** method is responsible for determining whether to listen or send data based on the command-line arguments. If the **`listen`** flag is provided, it calls the **`listen`** method; otherwise, it calls the **`send`** method.
5. The **`send`** method establishes a connection with the target specified in the command-line arguments. It sends the buffer (if provided) and enters a loop to receive data from the target. It prints the received data and prompts for user input to send back to the target.
6. The **`listen`** method binds the socket to the specified IP address and port, starts listening for incoming connections, and spawns a new thread for each client connection. The **`handle`** method is called in each new thread to handle the client connection.
7. The **`handle`** method receives a client socket and checks the command-line arguments to determine the action to perform. If the **`execute`** flag is provided, it executes the specified command and sends the output back to the client. If the **`upload`** flag is provided, it receives the file data from the client and saves it locally. If the **`command`** flag is provided, it sets up an interactive shell by continuously receiving commands from the client, executing them, and sending back the output.
8. The **`execute`** function is a helper function used to execute shell commands. It takes a command as input, strips any leading/trailing whitespace, and executes the command using the **`subprocess.check_output`** function. The output is returned as a string.
9. The **`if __name__ == '__main__':`** block is the entry point of the script. It sets up the command-line argument parser (**`argparse.ArgumentParser`**) and defines the available arguments (**`c`**, **`e`**, **`l`**, **`p`**, **`t`**, **`u`**). It also parses the provided arguments and determines whether to read from standard input or use a provided buffer based on the **`listen`** flag. Finally, it creates an instance of the **`NetCat`** class (**`nc`**) and calls its **`run`** method to start the NetCat tool.

Overall, this code allows you to use the NetCat tool to listen for incoming connections, send data to a specified target, execute commands, upload files, and interact with a command shell.
