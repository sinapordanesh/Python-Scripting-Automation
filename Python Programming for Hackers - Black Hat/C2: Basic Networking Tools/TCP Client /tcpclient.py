# Copyright (C) 2023 BLACK HAT PYTHON, Modified By Saman Pordanesh


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