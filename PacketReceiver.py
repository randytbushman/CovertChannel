import socket
import argparse


def decodePacket(packet):
    return chr(packet[12])


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)

    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--listener_port", help="The port we listen on")
    parser.add_argument("-i", "--server_address", help="The address of the VoIP server")
    parser.add_argument("-s", "--stealth", help="Number of packet encodings between each RTP transmission")
    parser.add_argument("-o", "--output", help="Output file location of message")
    parser.add_argument("-v", "--verbose", help="Prints each character to the stdout as it arrives")

    args = parser.parse_args()
    output = args.output

    serverAddress = args.server_address

    UDP_IP = get_ip()
    UDP_PORT = int(args.listener_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    message = ""
    while True:
        data, addr = sock.recvfrom(1024)    # buffer size is 1024 bytes
        char = decodePacket(data)
        message += char
        print(char, end="")

    if output is not None:
        f = open(output, 'w')
        f.write(message)
        f.close()


