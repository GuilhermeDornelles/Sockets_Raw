import re
import socket
from struct import unpack
from models.message import Message
from utils import format_and_validate_ip, format_and_validate_mac
import binascii


class ServerSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, protocol, data_port=12345, control_port=12346, source_mac="", dest_mac="", source_ip=""):
        self.socket_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.protocol = protocol
        self.data_port = data_port
        self.control_port = control_port
        self.config_socket(source_ip)
        self._format_and_validate_addresses(
            source_ip=source_ip, source_mac=source_mac, dest_mac=dest_mac)
        # TODO criar classe Chat para o protocolo de aplicacao
        # vai receber as mensagens e tratar, se são controle ou dados, gerenciar clientes conectados, e etc
        # self.chat = Chat()

    def config_socket(self, source_ip):
        self.socket_data.bind((source_ip, self.data_port))
        self.socket_control.bind((source_ip, self.control_port))

    def _format_and_validate_addresses(self, source_mac, dest_mac, source_ip):
        try:
            self.source_ip = format_and_validate_ip(source_ip)
            self.source_mac = format_and_validate_mac(source_mac)
            self.dest_mac = format_and_validate_mac(dest_mac)
        except Exception as err:
            # TODO
            # Formatar execuções com erro
            print("Erro ao formatar endereço: ", err)
            return

    def run_server(self):
        print(
            f"""Server's up! Listening on ports: 
                {self.data_port} for data messages
                {self.control_port} for control messages""")
        while True:
            try:
                data_pkt = self.socket_data.recvfrom(65535)
                # control_pkt = self.socket_control.recvfrom(65535)
                print(data_pkt)
                # if data_pkt is not None or control_pkt is not None:
                if data_pkt is not None:
                    if data_pkt:
                        new_message = self._open_package(package=data_pkt)
                    # else:
                    #     new_message = self._open_package(package=control_pkt)
                    # TODO
                    # chat.receive(new_message)
                    print(new_message)
            except KeyboardInterrupt:
                print("Server is shutting down...")
                self.stop_server()
                break
            except Exception as e:
                print(f"Erro ao receber pacote UDP: {e}")
        return True

    def stop_server(self):
        self.socket_data.close()
        self.socket_control.close()
        return

    def _open_package(self, package: tuple) -> Message:
        eth_header = package[0][0:14]

        # parsing using unpack
        # 6 dest MAC, 6 host MAC, 2 ethType
        eth_header = unpack("!6s6s2s", eth_header)

        # gambiarra do python pra transformar os macs em uma string com : separando cada byte
        bytes_src = binascii.hexlify(eth_header[0]).decode("utf-8")
        src_mac = ":".join(re.findall('..', bytes_src))
        bytes_dest = binascii.hexlify(
            eth_header[0]).decode("utf-8")
        dest_mac = ":".join(re.findall('..', bytes_dest))
        binascii.hexlify(eth_header[2])

        ip_header = package[0][14:34]
        # 12s represents Identification, Time to Live, Protocol | Flags, Fragment Offset, Header Checksum
        ip_header = unpack("!12s4s4s", ip_header)
        # network to ascii convertion
        src_ip = socket.inet_ntoa(ip_header[1])
        dest_ip = socket.inet_ntoa(ip_header[2])

        # unapck the TCP header (source and destination port numbers)
        udp_header = package[0][34:42]
        # H (unsigned short) = 2bytes
        udp_header = unpack("!4H", udp_header)
        src_port = udp_header[0]
        dest_port = udp_header[1]
        data = package[0][42:].decode("utf-8")
        return Message(source_mac=src_mac, dest_mac=dest_mac, source_ip=src_ip,
                       dest_ip=dest_ip, source_port=src_port, dest_port=dest_port, data=data)
