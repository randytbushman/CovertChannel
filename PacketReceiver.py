import socket
import argparse


def decodePacket(packet):
    return chr(packet[12])


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def startListener(sock, stealth):
    message = ""
    receivedPackets = 0
    while True:
        data, _ = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if receivedPackets == 0:
            message += decodePacket(data)
        receivedPackets = (1 + receivedPackets) % stealth
    return message


def startListenerV(sock, stealth):
    message = ""
    receivedPackets = 0
    while True:
        data, _ = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if receivedPackets == 0:
            char = decodePacket(data)
            message += char
            print(char, end="")
        receivedPackets = (1 + receivedPackets) % stealth
    return message


def startListenerVV(sock, stealth):
    print("vv mode")
    message = ""
    receivedPackets = 0
    i = 0
    while True:
        data, _ = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if receivedPackets == 0:
            char = decodePacket(data)
            message += char
            i += 1
            print(char, f"\t\tDecoded Packets #: {i}")
        receivedPackets = (1 + receivedPackets) % stealth
    return message


def startListenerVVV(sock, stealth):
    message = ""
    receivedPackets = 0
    i = 0
    while True:
        data, _ = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if receivedPackets == 0:
            char = decodePacket(data)
            message += char
            i += 1
            print(char, f"\t\tDecoded Packets #: {i}")
            print(f"Packet {i}: {data}\n\n")
        receivedPackets = (1 + receivedPackets) % stealth
    return message


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--listener_port", help="The port we listen on")
    parser.add_argument("-s", "--stealth", help="Number of packet encodings between each RTP transmission")
    parser.add_argument("-o", "--output", help="Output file location of message")
    parser.add_argument("-v", "--verbose", help="Prints each character to the stdout as it arrives", action='store_true')
    parser.add_argument("-vv", "--vverbose", help="Prints each character to the stdout as it arrives", action='store_true')
    parser.add_argument("-vvv", "--vvverbose", help="Prints each character to the stdout as it arrives", action='store_true')
    args = parser.parse_args()

    # Parse the arguments from the command line
    port = args.listener_port
    stealth = int(args.stealth)
    output = args.output

    UDP_IP = get_ip()
    UDP_PORT = int(args.listener_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    if args.vvverbose:
        message = startListenerVVV(sock, stealth)
    elif args.vverbose:
        message = startListenerVV(sock, stealth)
    elif args.verbose:
        message = startListenerV(sock, stealth)
    else:
        message = startListener(sock, stealth)

    sock.close()
    if output is not None:
        f = open(output, 'w')
        f.write(message)
        f.close()
