import socket
# from socket import AF_PACKET, SOCK_RAW
import struct
import re
import constants as constants


class RawSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, payload="", source_mac="", dest_mac="", source_ip="", dest_ip="", protocol=constants.UNKNOWN_TYPE, net_interface="eth0",):
        self.socket = socket.socket(
            socket.AF_PACKET, socket.SOCK_RAW, protocol)
        self.payload = "[ "+payload+" ]"
        self.protocol = protocol
        self._format_and_validate_addresses(
            source_mac, dest_mac, source_ip, dest_ip)
        self.set_interface(net_interface)
        self.eth_header = self._create_eth_header()

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
        pack = struct.pack("!6s6sH", self.dest_mac,
                           self.source_mac, protocol_type)
        return pack

    def _create_ip_protocol(self):
        # TODO
        # Criar a implementação do header de ip
        return True

    def _format_and_validate_mac(self, mac: str):
        aux_mac = mac.replace(":", "")
        if len(aux_mac) != 12:
            raise Exception
        if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
            raise Exception

        return bytes.fromhex(aux_mac)

    def _format_and_validate_ip(self, ip: str):
        # TODO
        return ip

    def send_package(self):
        # TODO
        # Concatenar outros headers e data conforme avançar a implementação
        self.socket.send(self.eth_header)
