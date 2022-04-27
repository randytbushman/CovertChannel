import socket
import argparse
import time


def decodePacket(payload):
    """
    Decodes the RTP packet payload and returns the encoded character.
    @return: the encoded character in the RTP packet
    """
    return chr(payload[12])


def get_ip():
    """
    Returns the host IP of this host.
    @return: a string representation of the ipv4 IP address
    """
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


def startListener(sock, stealth, messageLength):
    """
    Begins the listener and returns the information decoded from the packets.
    @param sock: the python socket object that the listener operates on
    @param stealth: the offset stealth value of the packet encodings
    @return: the decoded message
    """
    message = ""
    receivedPackets = 0
    i = 0
    totalPackets = stealth * messageLength
    while i < totalPackets:
        data, _ = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if receivedPackets == 0:
            message += decodePacket(data)
        receivedPackets = (1 + receivedPackets) % stealth
        i += 1
    sock.close()
    return message


def startListenerV(sock, stealth, messageLength):
    """
    Begins the listener in verbose mode 1 and returns the information decoded from the packets. Each decoded character
    is printed to the standard output.
    @param sock: the python socket object that the listener operates on
    @param stealth: the offset stealth value of the packet encodings
    @return: the decoded message
    """
    message = ""
    receivedPackets = 0
    i = 0
    totalPackets = stealth * messageLength
    while i < totalPackets:
        data, _ = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if receivedPackets == 0:
            char = decodePacket(data)
            message += char
            print(char, end="")
        receivedPackets = (1 + receivedPackets) % stealth
        i += 1
    sock.close()
    return message


def startListenerVV(sock, stealth, messageLength):
    """
    Begins the listener in verbose mode 2 and returns the information decoded from the packets. Each decoded character
    is printed to the standard output along with the time it takes for each packet to arrive.
    @param sock: the python socket object that the listener operates on
    @param stealth: the offset stealth value of the packet encodings
    @return: the decoded message
    """
    message = ""
    receivedPackets = 0
    numDecodedPackets = 0
    startTime = time.time()
    i = 0
    totalPackets = stealth * messageLength
    while i < totalPackets:
        data, _ = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if receivedPackets == 0:
            char = decodePacket(data)
            message += char
            numDecodedPackets += 1
            print(char, f"\t\tDecoded Packets #: {numDecodedPackets}", f"\t\tTimestamp: {time.time() - startTime}")
        receivedPackets = (1 + receivedPackets) % stealth
        i += 1
    sock.close()
    return message


def startListenerVVV(sock, stealth, messageLength):
    """
    Begins the listener in verbose mode 3 and returns the information decoded from the packets. Each decoded character
    is printed to the standard output along with the time it takes for each packet to arrive. The payload is also
    printed.
    @param sock: the python socket object that the listener operates on
    @param stealth: the offset stealth value of the packet encodings
    @return: the decoded message
    """
    message = ""
    receivedPackets = 0
    numDecodedPackets = 0
    startTime = time.time()
    i = 0
    totalPackets = stealth * messageLength
    while i < totalPackets:
        data, _ = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if receivedPackets == 0:
            char = decodePacket(data)
            message += char
            numDecodedPackets += 1
            print(char, f"\t\tDecoded Packets #: {numDecodedPackets}", f"\t\tTimestamp: {time.time() - startTime}")
            print(f"Packet {numDecodedPackets}: {data}\n\n")
        receivedPackets = (1 + receivedPackets) % stealth
        i += 1
    sock.close()
    return message


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--listener_port", help="The port we listen on.")
    parser.add_argument("-s", "--stealth", help="Number of packet encodings between each RTP transmission.")
    parser.add_argument("-o", "--output", help="Output file location for message.")
    parser.add_argument("-l", "--length", required=True, help="The length of the message we receive.")
    parser.add_argument("-v", "--verbose", help="Verbose mode 1.", action='store_true')
    parser.add_argument("-vv", "--vverbose", help="Verbose mode 2.", action='store_true')
    parser.add_argument("-vvv", "--vvverbose", help="Verbose mode 3.", action='store_true')
    args = parser.parse_args()

    # Parse the arguments from the command line
    port = args.listener_port
    stealth = int(args.stealth)
    output = args.output

    # Open and bind socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((get_ip(), int(args.listener_port)))

    # Select the listener function depending on verbosity value
    if args.vvverbose:
        message = startListenerVVV(sock, stealth, int(args.length))
    elif args.vverbose:
        message = startListenerVV(sock, stealth, int(args.length))
    elif args.verbose:
        message = startListenerV(sock, stealth, int(args.length))
    else:
        message = startListener(sock, stealth, int(args.length))

    # Save the message to the specified output location
    if output is not None:
        f = open(output, 'w')
        f.write(message)
        f.close()
