import socket
import argparse


def decodePacket(packet):
    return packet[66]


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
    parser.add_argument("-s", "--server_address", help="The address of the VoIP server")

    args = parser.parse_args()

    serverAddress = args.server_address

    UDP_IP = get_ip()
    UDP_PORT = 5000     # int(args.listener_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)    # buffer size is 1024 bytes
        print(decodePacket(data))


