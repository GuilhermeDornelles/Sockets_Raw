# from socket import socket, SOCK_RAW, AF_PACKET, htons
import socket
from socket import AF_PACKET, SOCK_RAW
import struct


class RawSocket:
    def __init__(self, payload, interface="eth0"):
        # self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.socket = socket.socket(AF_PACKET, SOCK_RAW)
        self.source_IP = '192.168.1.101'
        self.dest_IP = '192.168.1.1'
        self.source_MAC = "a4:1f:72:f5:90:52"
        self.dest_MAC = "a4:1f:72:f5:90:98"
        self.payload = "[ "+ payload +" ]"
        self.set_interface(interface)
        self.package = self._create_package()

    def set_interface(self, interface = "eth0"):
        self.socket.bind((interface, 0))

    def _format_MAC(self, mac_addr: str):
        mac_str = ""
        for item in mac_addr.split(":"):
            mac_str += "\x"+item
        return mac_str

    def _create_package(self):
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
        # eth_header = struct.pack("!6s6sH", b'\xa4\x1f\x72\xf5\x90\x52', b'\xa4\x1f\x72\xf5\x90\x98', 0x0800)
        dest_mac = self._format_MAC(self.dest_MAC)
        print(dest_mac)
        source_mac = self._format_MAC(self.source_MAC)
        print(source_mac)

        eth_header = struct.pack('!6B6BH', dest_mac[0], dest_mac[1], dest_mac[2], dest_mac[3], dest_mac[4], dest_mac[5], source_mac[0], source_mac[1], source_mac[2], source_mac[3], source_mac[4], source_mac[5], 0x080)
        
        ip_header = struct.pack("!6s6sH", b'\xa4\x1f\x72\xf5\x90\x52', b'\xa4\x1f\x72\xf5\x90\x98', 0x0800)
        package = eth_header
        sent = self.socket.send(package)
        print(sent)

        dst_mac = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
        # src_mac = [0x00, 0x0a, 0x11, 0x11, 0x22, 0x22]
        
        # # Ethernet header
        # eth_header = pack('!6B6BH', dst_mac[0], dst_mac[1], dst_mac[2], dst_mac[3], dst_mac[4], dst_mac[5], 
        #     src_mac[0], src_mac[1], src_mac[2], src_mac[3], src_mac[4], src_mac[5], 0x0800)
        
        # source_ip = '192.168.1.101'
        # dest_ip = '192.168.1.1'			# or socket.gethostbyname('www.google.com')
        
        # ip header fields
        
        # the ! in the pack format string means network order
        
        # build the final ip header (with checksum)
        
        # udp header fields
        
        # the ! in the pack format string means network order
        
        # final full packet - syn packets dont have any data
        # packet = eth_header + ip_header + ucp_header + dhcp_header
        # r = sendeth(packet, "enp1s0")

    
    def send_package(self):
        self.socket.send(self.package)
        # s = socket.socket(AF_PACKET, SOCK_RAW)
        # s.bind((interface, 0))
        # return s.send(eth_frame)
