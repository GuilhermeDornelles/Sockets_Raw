import socket
from utils import format_and_validate_ip


class ClientSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    # def __init__(self, dest_port: int, dest_ip: str, protocol=socket.SOCK_DGRAM):
    def __init__(self, dest_ip: str, protocol=socket.SOCK_DGRAM):

        # def __init__(self, data_port, control_port, dest_ip="", protocol=socket.SOCK_DGRAM):
        self.socket = socket.socket(socket.AF_INET, protocol)
        self.protocol = protocol
        # self.dest_port = dest_port
        # self.server_addr = (dest_ip, dest_port)
        self.dest_ip = dest_ip
        # self.dest_ip = format_and_validate_ip(dest_ip)
        self.connect_socket()

    def connect_socket(self):
        # self.socket.connect((dest_ip, dest_port))
        # buscando o IP e porta que sera usada como source
        source_port = self.socket.getsockname()[1]
        source_ip = self.socket.getsockname()[0]
        # TODO
        # fazer o socket client receber respostas tambem
        self.socket.bind((source_ip, source_port))

    def send_package(self, data: str, dest_port: int):
        package = data.encode("utf-8")
        self.socket.sendto(package, (self.dest_ip, dest_port))

    def close_socket(self):
        return self.socket.close()
