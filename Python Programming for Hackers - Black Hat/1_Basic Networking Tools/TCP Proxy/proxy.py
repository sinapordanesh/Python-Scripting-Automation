# Copyright (C) 2023 BLACK HAT PYTHON, Modified By Saman Pordanesh

import sys
import socket
import threading

# contains ASCII printable characters, if one exists, or a dot (.) if such a representation doesn’t exist.
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

"""
    hexdump() -> takes some input as bytes or a string and prints a hexdump to the console.
    output the packet details with both their hexadecimal values and ASCII-printable characters
"""
def hexdump(src, length=16, show=True): 
    # to make sure we have a string, decoding the bytes -> if byte string was passed in
    if isinstance(src, bytes): 
        src = src.decode()

    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length]) # grab a piece of the string to dump & put it into the word
        
        # substitute-> string representation of each character-> corresponding character in the raw string (printable)
        printable = word.translate(HEX_FILTER)
        # substitute the hex representation of the integer value of every character in the raw string (hexa)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        # array -> contains: {hex value of the index of the first byte in the word} {hex value of the word} {its printable representation}
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    
    if show:
        for line in results:
            print(line)
    else:
        return results

"""
    function that the two ends of the proxy will use to receive data
    arg: 'connection' -> socket object -> for receiving both local and remote data
 """
def receive_from(connection):

    # empty byte string -> buffer -> accumulate responses from the socket
    buffer = b"" 
    # connect timeout -> can be changed by case   
    connection.settimeout(5)    

    try:   
        # loop: read response data into the buffer 
        while True:     
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    # return the buffer byte string -> could be either the local or remote machine.
    return buffer   

"""
    modify the response/request packets before the proxy sends them
"""
def request_handler(buffer):
    # perform packet modifications
    return buffer
def response_handler(buffer):
    # perform packet modifications
    return buffer

""""
    This function contains the bulk of the logic for our proxy
"""
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # we connect to the remote host
    remote_socket.connect((remote_host, remote_port)) 

    # make sure we don’t need to first initiate a connection to the remote side and request data before going into the main loop
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
    
    # hand the output to the response_handler function
    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
        # send the received buffer to the local client
        client_socket.send(remote_buffer)

    """"
        loop to continually read from the local client, process the data, send it to
        the remote client, read from the remote client, process the data, and send it
        to the local client until we no longer detect any data.
    """
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>]Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        # no data to send -> cloce local/remote sockets -> break the loop
        if not len(local_buffer) or not len(remote_buffer): 
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


""""
    server_loop function to set up and manage the connection.
"""
def server_loop(local_host, local_port,
    remote_host, remote_port, receive_first):

    # create a socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        # bind the socket to the localhost and listening
        server.bind((local_host, local_port))
    except Exception as e:
        print('problem on bind: %r' % e)

        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)
    while True: 
        client_socket, addr = server.accept()
        # print out the local connection information
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)
        # start a thread to talk to the remote host -> does all of the sending and receiving of juicy bits to either side of the data stream.
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host,
            remote_port, receive_first))
        proxy_thread.start()

"""
    In the main function, we take in some command line arguments and then fire up the server loop that listens for connections.    
    We need 5 arguments to pass to the terminal: local_host, local_port, remote_host, remote_port, receive_first
"""
def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port,
    remote_host, remote_port, receive_first)


# Start the server
if __name__ == "__main__":
    main()