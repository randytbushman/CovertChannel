import socket
import argparse


def decodePacket(packet):
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--listener_port", help="The port we listen on")
    parser.add_argument("-s", "--server_address", help="The address of the VoIP server")
    args = parser.parse_args()

    serverAddress = args.server_address

    UDP_IP = "127.0.0.1"
    UDP_PORT = int(args.listener_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if addr == serverAddress:
            print(decodePacket(data), end="")

