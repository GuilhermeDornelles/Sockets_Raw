from socket import socket, SOCK_RAW, AF_PACKET, htons
import struct


class RawSocket:
    def __init__(self, protocol=0x0800):
        self.socket = socket(AF_PACKET, SOCK_RAW, htons(protocol))
        self.source_addresses = ""
        self.dest_addresses = ""
        self.payload = ("["*30)+"PAYLOAD"+("]"*30)
        self.set_interface(protocol)
        pass

    def set_interface(self, protocol):
        self.socket.bind("eth0", htons(protocol))

    def create_package(self):
        # 6 dest address, 6 source address and 2 for ethtype = IP
        struct.pack("!6s6s2s", '\xaa\xaa\xaa\xaa\xaa\xaa',
                    '\xbb\xbb\xbb\xbb\xbb\xbb', '\x08\x00')
