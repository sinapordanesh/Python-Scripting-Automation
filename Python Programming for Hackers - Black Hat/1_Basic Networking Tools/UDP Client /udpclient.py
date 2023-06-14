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