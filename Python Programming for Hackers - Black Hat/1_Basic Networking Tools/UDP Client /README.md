
# UDP Client

## Code

```python
import socket

target host = "127.0.0.1"
target port = 9997

#1 create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#2 send some data
client.sendto(b"AAABBBCCC", (target_host‚target_port))

#3 receive some data
data, addr = client.recvfrom (4096)
print (data.decode())
client.close ()
```

## Explanation

As you can see, we change the socket type to `SOCK_DGRAM` `1` when creating the socket object. The next step is to simply call sendto() `2`, passing in the data and the server you want to send the data to. Because UDP is a connectionless protocol, there is no call to connect() beforehand. The last step is to call recvfrom() `3` to receive UDP data back. You will also notice that it returns both the data and the details of the remote host and port.
