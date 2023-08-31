import random
import socket
# from socket import AF_PACKET, SOCK_RAW
from struct import pack
import re
import constants as constants


class RawSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, source_mac="", dest_mac="", source_ip="", dest_ip="", protocol=constants.RAW_TYPE, net_interface="eth0",):
        self.socket = socket.socket(
            socket.AF_PACKET, socket.SOCK_RAW, protocol)
            # socket.AF_INET, socket.SOCK_RAW, protocol)
        # self.payload = "[ "+payload+" ]"
        self.protocol = protocol
        self._format_and_validate_addresses(
            source_mac, dest_mac, source_ip, dest_ip)
        self.set_interface(net_interface)
        # self.eth_header = self._create_eth_header()

    def _format_and_validate_addresses(self, source_mac, dest_mac, source_ip, dest_ip):
        try:
            self.source_ip = self._format_and_validate_ip(source_ip)
            self.dest_ip = self._format_and_validate_ip(dest_ip)
            self.source_mac = self._format_and_validate_mac(source_mac)
            self.dest_mac = self._format_and_validate_mac(dest_mac)
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
        pack = pack("!6s6sH", self.dest_mac,
                           self.source_mac, protocol_type)
        return pack

    def _create_ip_protocol(self, data_len):
        # TODO TESTAR
        # referencia: https://github.com/vinayrp1/TCP-IP-implementation-using-RAW-sockets/blob/master/rawhttpget.py
        
        # constants for IP header
        IHL = 5
        IP_VERSION = 4
        TYPE_OF_SERVICE = 0
        DONT_FRAGMENT = 0
        IP_HDR_LEN = 20
        TCP_HDR_LEN = 20
        # MIN_TOTAL_LENGTH = IP_HDR_LEN + TCP_HDR_LEN
        FRAGMENT_STATUS = DONT_FRAGMENT
        TIME_TO_LIVE = 255
        PROTOCOL = socket.IPPROTO_UDPLITE 
        # TODO PROTOCOL = socket.IPPROTO_TCP
        src_IP = self.source_ip
        dest_IP = self.dest_ip
        pktID = random.randint(10000,50000) 							# some random number as ID in IP hdr
        check_sum_of_hdr = 0 
        total_len = IP_HDR_LEN + data_len 
        IHL_VERSION = IHL + (IP_VERSION << 4) 
        ip_header = pack('!BBHHHBBH4s4s' , IHL_VERSION, TYPE_OF_SERVICE, total_len, pktID, FRAGMENT_STATUS, TIME_TO_LIVE, PROTOCOL, check_sum_of_hdr, src_IP, dest_IP)
        # TODO TESTAR check_sum_of_hdr = get_checksum(IP_header)
        ip_header = pack('!BBHHHBBH4s4s' , IHL_VERSION, TYPE_OF_SERVICE, total_len, pktID, FRAGMENT_STATUS, TIME_TO_LIVE, PROTOCOL, check_sum_of_hdr, src_IP, dest_IP)	
        return ip_header

    def _format_and_validate_mac(self, mac: str):
        aux_mac = mac.replace(":", "")
        try:
            if len(aux_mac) != 12:
                raise Exception
            if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
                raise Exception

            result = bytes.fromhex(aux_mac)
        except Exception as e:
            raise e
        return result

    def _format_and_validate_ip(self, ip: str):
        aux_ip = ip.replace(".", "")
        try:
            int(aux_ip)
            if not re.match("^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", ip.lower()):
                raise Exception
            
            result = socket.inet_aton(ip)
        except Exception as e: 
            raise e
        return result

    def send_package(self, data: str):
        # TODO
        # Concatenar outros headers e data conforme avançar a implementação
        
        # tcp_headers = self._create_tcp_header()
        # udp_headers = self._create_udp_headers()
        ip_headers = self._create_ip_header(data_len = len(data))
        eth_header = self._create_eth_header()
        # headers = eth_header + ip_header + tcp_header
        headers = eth_header + ip_headers

        package = headers + data

        self.socket.send(package)
