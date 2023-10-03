import socket
import threading
import time
from utils import format_and_validate_ip, super_print


class ClientSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, dest_ip: str, protocol=socket.SOCK_DGRAM):
        self.socket = socket.socket(socket.AF_INET, protocol)
        self.protocol = protocol
        # self.dest_port = dest_port
        self.dest_ip = dest_ip
        self.connect_socket()

    def start(self):
        thread_receiver = threading.Thread(
            target=self._start_receive, args=(), daemon=True)
        thread_receiver.start()
        time.sleep(1)

    def connect_socket(self):
        source_port = self.socket.getsockname()[1]
        source_ip = self.socket.getsockname()[0]
        self.socket.bind((source_ip, source_port))

    def send_package(self, data: str, dest_port: int):
        package = data.encode("utf-8")
        self.socket.sendto(package, (self.dest_ip, dest_port))

    def close_socket(self):
        return self.socket.close()

    def _open_package(self, package: tuple) -> str:
        data = package[0].decode("utf-8")
        return data

    def _start_receive(self):
        port = self.socket.getsockname()[1]
        while True:
            print(f"Client is receiving messages on port {port}")
            package = self.socket.recvfrom(1024)
            print(f"Nova mensagem de {self._open_package(package)}")
