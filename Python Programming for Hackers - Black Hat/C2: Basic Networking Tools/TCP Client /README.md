# TCP Client

## Code

```python
import socket

target_host = "www.google.com"
target_port = 80

#1 Create a socket object
client = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

#2 connect the client
client.connect((target_host,target_port))

#3 send some data
client.send(b"GET / HTTP/1.1\rInHost: google.com\r\n\r\n")

#4 receive some data
response = client.recv(4096)
print(response.decode ())
client.close()
```

## Explanation

We first create a socket object with the `AF_INET` and `SOCK_STREAM` parameters `1`. The `AF_INET` parameter indicates we’ll use a standard IPv4 address or hostname, and `SOCK_STREAM` indicates that this will be a TCP client. We
then connect the client to the server `2` and send it some data as bytes `3`. The last step is to receive some data back and print out the response `4` and then close the socket. This is the simplest form of a TCP client, but it’s the one you’ll write most often.
