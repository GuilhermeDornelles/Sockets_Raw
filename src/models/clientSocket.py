import random
import socket
from struct import pack
import re
from utils import format_and_validate_ip, format_and_validate_mac, get_checksum


class ClientSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, source_port, dest_port, protocol, source_mac="", dest_mac="", source_ip="", dest_ip="", net_interface="eth0"):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.protocol = protocol
        self.source_port = source_port
        self.dest_port = dest_port
        self._format_and_validate_addresses(
            source_mac, dest_mac, source_ip, dest_ip)
        self.connect_socket(dest_ip, dest_port)

    def _format_and_validate_addresses(self, source_mac, dest_mac, source_ip, dest_ip):
        try:
            self.source_ip = format_and_validate_ip(source_ip)
            self.dest_ip = format_and_validate_ip(dest_ip)
            self.source_mac = format_and_validate_mac(source_mac)
            self.dest_mac = format_and_validate_mac(dest_mac)
        except Exception as err:
            # TODO
            # Formatar execuções com erro
            print("Erro ao formatar endereço: ", err)
            raise Exception

    def connect_socket(self, dest_ip, dest_port):
        self.socket.connect((dest_ip, dest_port))

    def _create_eth_header(self):
        # 6 dest address, 6 source address and 2 for ethtype = IP
        protocol_type = self.protocol

        # 6 bytes for destination mac
        # 6 bytes for source mac
        # 1 int for protocol type
        pkg = pack("!6s6sH", self.dest_mac,
                   self.source_mac, protocol_type)
        return pkg

    def _create_ip_header(self, data):
        # TODO
        # FRAGMENTAR IP

        # referencia: https://github.com/vinayrp1/TCP-IP-implementation-using-RAW-sockets/blob/master/rawhttpget.py
        # constants for IP header
        DATA_LEN = len(data.encode("utf-8"))
        IHL = 5
        IP_VERSION = 4
        TYPE_OF_SERVICE = 0
        DONT_FRAGMENT = 0
        IP_HDR_LEN = 20
        UDP_LEN = 8 + DATA_LEN
        FRAGMENT_STATUS = DONT_FRAGMENT
        TIME_TO_LIVE = 255
        PROTOCOL = socket.IPPROTO_UDP
        pkt_id = random.randint(10000, 50000)
        checksum = 0
        total_len = IP_HDR_LEN + UDP_LEN
        IHL_VERSION = IHL + (IP_VERSION << 4)

        ip_header = pack('!BBHHHBBH4s4s', IHL_VERSION, TYPE_OF_SERVICE, total_len,
                         pkt_id, FRAGMENT_STATUS, TIME_TO_LIVE, PROTOCOL, checksum, self.source_ip, self.dest_ip)

        checksum = get_checksum(ip_header)

        ip_header = pack('!BBHHHBBH4s4s', IHL_VERSION, TYPE_OF_SERVICE, total_len,
                         pkt_id, FRAGMENT_STATUS, TIME_TO_LIVE, PROTOCOL, checksum, self.source_ip, self.dest_ip)

        return ip_header

    def _create_udp_header(self, data=None):
        PROTOCOL = socket.IPPROTO_UDP
        SRC_PORT = self.source_port
        DEST_PORT = self.dest_port
        SRC_IP = self.source_ip
        DEST_IP = self.dest_ip
        data = data.encode()
        FINAL_LEN = 8 + len(data)
        checksum = 0

        header = SRC_IP + DEST_IP + pack('!BBH', 0, PROTOCOL, FINAL_LEN)
        udp_header = pack('!4H', SRC_PORT, DEST_PORT, FINAL_LEN, checksum)
        checksum = get_checksum(header + udp_header + data)
        udp_header = pack('!4H', SRC_PORT, DEST_PORT, FINAL_LEN, checksum)
        return udp_header

    def send_package(self, data: str):
        # TODO
        # Concatenar outros headers e data conforme avançar a implementação
        eth_header = self._create_eth_header()
        ip_headers = self._create_ip_header(data)
        udp_header = self._create_udp_header(data)
        headers = eth_header + ip_headers + udp_header

        package = headers + data.encode("utf-8")
        self.socket.send(package)

    def close_socket(self):
        return self.socket.close()
