import socket
from models.message import Command

class ChatServerSocket:
    def __init__(self, data_port=12345, source_ip=""):
        self.socket_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_port = data_port
        self.source_ip = source_ip
        self.new_package = None

    def bind_server(self):
        self.socket_data.bind((self.source_ip, self.data_port))

    def receive_package(self) -> Command:
        try:
            self.socket_data.listen()
            connection, addr = self.socket_data.accept()
            data = connection.recv(1024)
            connection.close()
            new_message = self._open_package(data, addr)
            return new_message
        except KeyboardInterrupt:
            return None

    def stop_server(self):
        self.socket_data.close()

    def _open_package(self, data: bytes, addr: tuple) -> Command:
        ip = addr[0]
        port = addr[1]
        return Command(source_ip=ip, source_port=port, data=data.decode("utf-8"))

class ControlServerSocket:
    def __init__(self, control_port=12346, source_ip=""):
        self.socket_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.control_port = control_port
        self.source_ip = source_ip
        self.new_package = None

    def bind_server(self):
        self.socket_control.bind((self.source_ip, self.control_port))

    def receive_package(self) -> Command:
        try:
            new_package = self.socket_control.recvfrom(1024)
            new_message = self._open_package(new_package)
            return new_message
        except KeyboardInterrupt:
            return None

    def stop_server(self):
        self.socket_control.close()

    def _open_package(self, package: tuple) -> Command:
        data = package[0].decode("utf-8")
        ip = package[1][0]
        port = package[1][1]
        return Command(source_ip=ip, source_port=port, data=data)
