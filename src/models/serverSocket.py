import socket
import threading
import time
from models.client import Client
from models.command import Command
from utils import format_and_validate_ip


class ServerSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, protocol, port=12345, source_ip=""):
        self.socket = socket.socket(socket.AF_INET, protocol)
        self.protocol = protocol
        self.bind_server(source_ip, port)
        self.port = port

    def bind_server(self, source_ip, port):
        self.socket.bind((source_ip, port))

    def receive_package(self) -> Command:
        package = self.socket.recvfrom(1024)
        print("Opening package")
        new_message = self._open_package(package=package)
        return new_message

    def stop_server(self):
        print(f"Socket on port {self.port} is shutting down..")
        self.socket.close()

    def _open_package(self, package: tuple) -> Command:
        data = package[0].decode("utf-8")
        ip = package[1][0]
        port = package[1][1]
        return Command(source_ip=ip, source_port=port, data=data)

    def send_package(self, text: str, client: Client):
        text = text.encode("utf-8")
        return self.socket.sendto(text, (client.ip, client.port))
