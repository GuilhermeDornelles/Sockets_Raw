import socket
from utils import format_and_validate_ip


class ClientSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, dest_port, dest_ip="", protocol=socket.SOCK_DGRAM):
        self.socket = socket.socket(socket.AF_INET, protocol)
        self.protocol = protocol
        self.dest_port = dest_port
        self.dest_ip = format_and_validate_ip(dest_ip)
        self.connect_socket(dest_ip, dest_port)

    def connect_socket(self, dest_ip, dest_port):
        self.socket.connect((dest_ip, dest_port))

    def send_package(self, data: str):
        package = data.encode("utf-8")
        self.socket.send(package)

    def close_socket(self):
        return self.socket.close()
