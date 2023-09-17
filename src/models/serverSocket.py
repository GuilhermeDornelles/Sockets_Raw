import socket
from struct import unpack
from utils import format_and_validate_ip, format_and_validate_mac
import binascii


class ServerSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, protocol, source_port=61, source_mac="", dest_mac="", source_ip=""):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.protocol = protocol
        self.source_port = source_port
        self.config_socket(source_ip)
        self._format_and_validate_addresses(
            source_ip=source_ip, source_mac=source_mac, dest_mac=dest_mac)

    def config_socket(self, source_ip):
        self.socket.bind((source_ip, self.source_port))

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
        print("Server's up! Listen in port: {0}".format(self.source_port))
        while True:
            try:
                pkt = self.socket.recvfrom(65535)
                if pkt is not None:
                    print('*****************************')
                    print('** Informações da mensagem **')
                    print('*****************************')
                    eth_header = pkt[0][0:14]

                    # parsing using unpack
                    # 6 dest MAC, 6 host MAC, 2 ethType
                    eth_header = unpack("!6s6s2s", eth_header)

                    # using hexify to convert the tuple value NBO into Hex format
                    binascii.hexlify(eth_header[0])
                    binascii.hexlify(eth_header[1])
                    binascii.hexlify(eth_header[2])

                    ip_header = pkt[0][14:34]
                    # 12s represents Identification, Time to Live, Protocol | Flags, Fragment Offset, Header Checksum
                    ip_header = unpack("!12s4s4s", ip_header)

                    # network to ascii convertion
                    print(f"Source IP addr: {socket.inet_ntoa(ip_header[1])}")
                    # network to ascii convertion
                    print(
                        f"Destination IP addr: {socket.inet_ntoa(ip_header[2])}")

                    # unapck the TCP header (source and destination port numbers)
                    udp_header = pkt[0][34:42]
                    # H (unsigned short) = 2bytes
                    udp_header = unpack("!4H", udp_header)
                    print(f"Source Port: {udp_header[0]}")
                    print(f"Destination Port: {udp_header[1]}")
                    data = pkt[0][42:]
                    print(f"Message is: {data}")
            except KeyboardInterrupt:
                print("Server is shutting down...")
                self.stop_server()
                break
            except Exception as e:
                print(f"Erro ao receber pacote UDP: {e}")
        return True

    def stop_server(self):
        return self.socket.close()
