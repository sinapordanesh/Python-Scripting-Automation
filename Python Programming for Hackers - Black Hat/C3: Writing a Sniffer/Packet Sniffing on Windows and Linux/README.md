# Packet Sniffing on Windows and Linux**

## `sniffer.py`

```python
import socket
import os

# host to listen on
HOST = '127.0.0.1'

def main():
    # create raw socket, bind to public interface
    if os.name == 'nt': # checks if os is withndows
        socket_protocol = socket.IPPROTO_ICMP
    else:
        socket_protocol = socket.IPPROTO_IP

    # socket object with the parameters necessary for sniffing packets on our network interface
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))

    # include the IP header in the capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # read one packet
    print(sniffer.recvfrom(65565)) # printing out the entire raw packet

    if os.name == 'nt': # checks if os is withndows
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF) # disable promiscuous mode

if __name__ == '__main__':
    main()
```

The code above is a Python script that demonstrates how to capture and print out the contents of a single packet on a network interface. The script uses the `socket` module to create a raw socket and bind it to the public interface. It then sets the `IP_HDRINCL` option to include the IP header in the packet capture, reads one packet using `sniffer.recvfrom(65565)`, and prints out the entire raw packet in hexadecimal format. If the OS is Windows, the script enables promiscuous mode using `sniffer.ioctl()` and `RCVALL_ON` before reading the packet, and disables it using `sniffer.ioctl()` and `RCVALL_OFF` after reading the packet.

Here are more details on how the code works:

- The script imports the necessary modules, `socket` and `os`
- It sets the IP address of the host to listen to `127.0.0.1` (localhost)
- It checks the operating system and sets the `socket_protocol` to `socket.IPPROTO_ICMP` if the OS is Windows and `socket.IPPROTO_IP` if it's Linux.
- It creates a raw socket using `socket.socket()` with the parameters necessary for sniffing packets on the network interface.
- It binds the socket to the public interface using `sniffer.bind()`
- It sets the `IP_HDRINCL` option to include the IP header in the capture using `sniffer.setsockopt()`
- If the OS is Windows, it sets the `SIO_RCVALL` option to `RCVALL_ON` to enable promiscuous mode using `sniffer.ioctl()`.
- It reads one packet using `sniffer.recvfrom(65565)` and prints out the entire raw packet in hexadecimal format.
- If the OS is Windows, it disables promiscuous mode using `sniffer.ioctl()` and `RCVALL_OFF` after reading the packet.

## ***Kicking the Tires***

- This code is for **windows**

Run a fresh CMD in Administrator mode and run the code:

```powershell
python sniffer.py
```

Ping a website in another command promp:

```powershell
ping google.com
```

The output should be like this:

```powershell
(b'E\x00\x00T\xad\xcc\x00\x00\x80\x01\n\x17h\x14\xd1\x03\xac\x10\x9d\x9d\x00\x00g,\rv\x00\x01\xb6L\x1b^\x00\x00\x00\x00\xf1\xde\t\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f!"#$%&\'()*+,-./01234567', ('104.20.209.3', 0))
```
