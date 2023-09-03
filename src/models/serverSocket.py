

import socket

from src.constants import RAW_TYPE, format_and_validate_ip, format_and_validate_mac


class ServerSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, source_mac="", dest_mac="", source_ip="", dest_ip="", source_port=0, dest_port=0, protocol=RAW_TYPE, net_interface="eth0",):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
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
        
    def receive_packet(self):
        source_ip = ""
        dest_port = ""
        # loop until we get the packet destined for our port and IP addr
        while (source_ip != str(self.source_port) and dest_port != str(self.source_port) or source_ip != "" and dest_port != ""):
            recvPacket = self.socket.recv(65565)
            ipHeader=recvPacket[0:20]
            ipHdr=unpack("!2sH8s4s4s",ipHeader)					#unpacking to get IP header
            source_ip=socket.inet_ntoa(ipHdr[3])
            tcpHeader=recvPacket[20:40]						#unpacking to get TCP header
            tcpHdr=unpack('!HHLLBBHHH',tcpHeader)
            dest_port=str(tcpHdr[1])
            destinationIP = ""
            dest_port = ""
        return recvPacket

