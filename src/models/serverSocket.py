import socket
from struct import unpack
from utils import format_and_validate_ip, format_and_validate_mac
import binascii


class ServerSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, source_port, dest_port, protocol, source_mac="", dest_mac="", source_ip="", dest_ip=""):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.protocol = protocol
        self.source_port = source_port
        self.dest_port = dest_port
        self.config_socket(source_ip)

    def config_socket(self, source_ip):
        self.socket.bind((source_ip, self.source_port))

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

                    print("Source IP address %s" % socket.inet_ntoa(
                        ip_header[1]))  # network to ascii convertion
                    print("Destination IP address %s" % socket.inet_ntoa(
                        ip_header[2]))  # network to ascii convertion

                    # unapck the TCP header (source and destination port numbers)
                    udp_header = pkt[0][34:54]
                    udp_header = unpack("!HH16s", udp_header)

                    print("Source Source Port: %s" % udp_header[0])
                    print("Source Destination Port: %s" % udp_header[1])
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Erro ao receber pacote UDP: {e}")
        return True

    def stop_server(self):
        return self.socket.close()
