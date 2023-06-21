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
