# from socket import socket, SOCK_RAW, AF_PACKET, htons
import socket
import struct


class RawSocket:
    def __init__(self, protocol=0x0800):
        self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.source_addresses = ""
        self.dest_addresses = ""
        self.payload = "[ "+"PAYLOAD"+" ]"
        self.set_interface(protocol)
        self.package = self._create_package()

        

    def set_interface(self, protocol):
        self.socket.bind("eth0", socket.IPPROTO_IP)

    def create_package(self):
        version = 4
        ihl = 5
        tos = 0
        length = 20 +len(self.payload)
        id = 0
        offset = 0
        ttl = 255
        checksum = 0
        flags = 0

        ver_ihl = (version << 4) + ihl
        flags_offset = (flags << 13) + offset

        # 6 dest address, 6 source address and 2 for ethtype = IP
        pack = struct.pack("!6s6sH", b'\xa4\x1f\x72\xf5\x90\x52', b'\xa4\x1f\x72\xf5\x90\x98', 0x0800)
        package = pack
        sent = self.socket.send(package)
        print(sent)

    
    def send_package(self):
        self.socket.send(self.package)
