import socket
import threading
import time
from models.client import Client
from models.command import Command
from utils import format_and_validate_ip
from abc import ABC, abstractmethod


class ServerSocket(ABC):

    @abstractmethod
    def receive_package(self) -> Command:
        pass

    @abstractmethod
    def stop_server(self):
        pass

    @abstractmethod
    def send_package(self, text: str, client: Client):
        pass


class ServerSocketUDP(ServerSocket):
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
        try:
            self.socket.sendto(text.encode("utf-8"), (client.ip, client.port))
        except Exception:
            return False
        return True


class ServerSocketTCP(ServerSocket):
    def __init__(self, protocol, port=12345, source_ip=""):
        self.socket = socket.socket(socket.AF_INET, protocol)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.protocol = protocol
        self.bind_server(source_ip, port)
        self.port = port

    def bind_server(self, source_ip, port):
        self.socket.bind((source_ip, port))
        self.socket.listen(1)

    def receive_package(self) -> Command:
        connection, _addr = self.socket.accept()
        print("accept()")
        package = connection.recv(1024)
        # package = self.socket.recvfrom(1024)
        print(f"Opening package {package}")
        new_message = self._open_package(package=package, addr=_addr)
        # new_message = self._open_package(package=package)
        return new_message

    def stop_server(self):
        print(f"Socket on port {self.port} is shutting down..")
        self.socket.close()

    # def _open_package(self, package) -> Command:
    #     data = package[0].decode("utf-8")
    #     ip = package[0][0]
    #     port = package[1][1]
    #     return Command(source_ip=ip, source_port=port, data=data)

    def _open_package(self, package, addr) -> Command:
        data = package.decode("utf-8")
        ip = addr[0]
        port = addr[1]
        return Command(source_ip=ip, source_port=port, data=data)

    # def connect_to_client(self, client):
    #     self.socket.connect((client.ip, client.port))

    def send_package(self, text: str, client: Client):
        try:
            # connection, _addr = self.socket.connect((client.ip, client.port))
            sent = self.socket.sendto(text.encode(
                "utf-8"), (client.ip, client.port))
            print(f"sent {sent}")
            # connection.close()
        except Exception:
            return False
        return True
