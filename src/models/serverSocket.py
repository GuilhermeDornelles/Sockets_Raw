from socket import SOCK_DGRAM, SOCK_STREAM
import socket
from models.client import Client
from models.command import Command


class ServerSocket:
    def __init__(self, protocol, port=12345, source_ip=""):
        self.socket = socket.socket(socket.AF_INET, protocol)
        self.protocol = protocol
        self.port = port
        self.config_socket(source_ip, port)

    def config_socket(self, source_ip, port):
        self.socket.bind((source_ip, port))
        # self.socket.listen(1)

    def receive_package(self) -> Command:
        try:
            if self.socket.type == SOCK_DGRAM:
                package = self.socket.recvfrom(1024)
                if package is not None:
                    print("Opening package:")
                    new_message = self._open_package_udp(package=package)
                    return new_message
                else:
                    print("No package")
            else:
                print("listen()")
                connection, addr = self.socket.accept()
                print("accept()")
                package = connection.recv(1024)
                print("recv()")
                if package is not None:
                    print("Opening package:")
                    new_message = self._open_package_tcp(
                        package=package, connection=addr)
                    # Fecha a conexão após abrir pacote
                    connection.close()
                    return new_message
                else:
                    print("No package")

            return None
        except Exception as e:
            print(e)

    def stop_server(self):
        print(f"Socket on port {self.port} is shutting down..")
        self.socket.close()

    def _open_package_tcp(self, package, connection):
        data = package.decode("utf-8")
        ip = connection[0]
        port = connection[1]
        return Command(source_ip=ip, source_port=port, data=data)

    def _open_package_udp(self, package: tuple) -> Command:
        data = package[0].decode("utf-8")
        ip = package[1][0]
        port = package[1][1]
        return Command(source_ip=ip, source_port=port, data=data)

    def send_package(self, text: str, client: Client):
        try:
            if self.socket.type == SOCK_STREAM:
                pass
                # self.socket.connect((client.ip, client.port))
            self.socket.sendto(text.encode("utf-8"), (client.ip, client.port))
        except Exception:
            return False
        return True
