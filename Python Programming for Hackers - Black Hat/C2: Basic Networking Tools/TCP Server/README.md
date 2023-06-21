# TCP Server

## Code

```python
import socket 
import threading

IP = '127.0.0.1'
PORT = 9998

def main():
	server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	server.bind((IP, PORT)) #1 
	server.listen(5) #2
	print (f'[*] Listening on {IP}: {PORT}')
	
	while True:
		client, address = server.accept() #3
		print (f'[*] Accepted connection from {address [ol]}:{address[1]}')
		client_handler = threading.Thread(target=handle_client, args=(client,))
		client_handler.start() #4

def handle_client(client_socket): #5 
	with client_socket as sock:
		request = sock.recv(1024)
		print (f'[*] Received: {request.decode("utf-8")}')
		sock.send(b'ACK')

if __name__ == '__main__':
	main()
```

## Explanation

To start off, we pass in the IP address and port we want the server to listen on `1`. Next, we tell the server to start listening `2`, with a maximum backlog of connections set to 5. We then put the server into its main loop, where it waits for an incoming connection. When a client connects `3`, we receive the client socket in the client variable and the remote connection details in the address variable. We then create a new thread object that points to our `handle_client` function, and we pass it the client socket object as an argument. We then start the thread to handle the client connection `4`, at which point the main server loop is ready to handle another incoming connection. The `handle_client` function `5` performs the `recv()` and then sends a simple message back to the client. 
