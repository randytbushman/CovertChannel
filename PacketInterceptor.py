import argparse
import base64
import queue
import time
import scapy.all as scapy


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", help="String message to send")
    parser.add_argument("-f", "--filename", help="File to send")
    parser.add_argument("-s", "--stealth", help="Number of packet encodings between each RTP transmission")
    parser.add_argument("-d", "--destination", help="The destination ipv4 address")
    args = parser.parse_args()

    if args.filename is not None:
        file = open(args.filename, 'rb')
        transmissionString = base64.b64encode(file.read())
        file.close()
    else:
        transmissionString = args.message

    packetQ = queue.Queue()
    asyncSniffer = scapy.AsyncSniffer(prn=lambda x: packetQ.put(x))
    asyncSniffer.start()

    while True:
        if packetQ.qsize() > 0:
            print(packetQ.get().summary())

    asyncSniffer.stop()

    # results = scapy.sniff(count=10, prn=lambda x: x.summary())
    '''encodedPacketsCount = 0
    stealthCount = 0
    while encodedPacketsCount < len(transmissionString):
        if not packetQ.empty():
            p = packetQ.get()
            stealthCount += 1
            if stealthCount % args.stealth == 0:
                pass #Encode packet
            # Send packet'''


