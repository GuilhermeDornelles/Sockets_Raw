import random
import socket
# from socket import AF_PACKET, SOCK_RAW
from struct import pack
import re
import constants as constants
from constants import format_and_validate_ip, format_and_validate_mac, get_checksum


class ClientSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, source_mac="", dest_mac="", source_ip="", dest_ip="", source_port=0, dest_port=0, protocol=constants.RAW_TYPE, net_interface="eth0",):
        self.socket = socket.socket(
            socket.AF_PACKET, socket.SOCK_RAW, protocol)
        self.protocol = protocol
        self.source_port = source_port
        self.dest_port = dest_port
        self._format_and_validate_addresses(
            source_mac, dest_mac, source_ip, dest_ip)
        self.set_interface(net_interface)

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

    def set_interface(self, interface):
        self.socket.bind((interface, 0))

    def _create_eth_header(self):
        # 6 dest address, 6 source address and 2 for ethtype = IP
        protocol_type = self.protocol

        # 6 bytes for destination mac
        # 6 bytes for source mac
        # 1 int for protocol type
        pkg = pack("!6s6sH", self.dest_mac,
                   self.source_mac, protocol_type)
        return pkg

    def _create_ip_header(self):
        # referencia: https://github.com/vinayrp1/TCP-IP-implementation-using-RAW-sockets/blob/master/rawhttpget.py
        # constants for IP header
        IHL = 5
        IP_VERSION = 4
        TYPE_OF_SERVICE = 0
        DONT_FRAGMENT = 0
        IP_HDR_LEN = 20
        FRAGMENT_STATUS = DONT_FRAGMENT
        TIME_TO_LIVE = 255

        # TODO Fazer um handler que controla se vai usar tcp ou udp
        PROTOCOL = socket.IPPROTO_UDP
        pkt_id = random.randint(10000, 50000)
        checksum = 0
        total_len = IP_HDR_LEN  # + data_len
        IHL_VERSION = IHL + (IP_VERSION << 4)

        ip_header = pack('!BBHHHBBH4s4s', IHL_VERSION, TYPE_OF_SERVICE, total_len,
                         pkt_id, FRAGMENT_STATUS, TIME_TO_LIVE, PROTOCOL, checksum, self.source_ip, self.dest_ip)

        checksum = get_checksum(ip_header)

        ip_header = pack('!BBHHHBBH4s4s', IHL_VERSION, TYPE_OF_SERVICE, total_len,
                         pkt_id, FRAGMENT_STATUS, TIME_TO_LIVE, PROTOCOL, checksum, self.source_ip, self.dest_ip)

        return ip_header

    def _create_tcp_or_udp_header(self, data=None):
        pass

    def send_package(self, data: str):
        # TODO
        # Concatenar outros headers e data conforme avançar a implementação

        ip_headers = self._create_ip_header() #data_len=len(data.encode("utf-8")))
        eth_header = self._create_eth_header()
        tcp_udp_header = self._create_tcp_or_udp_header()
        # headers = eth_header + ip_header + tcp_header
        headers = eth_header + ip_headers

        package = headers  # + data.encode("utf-8")

        self.socket.send(package)
