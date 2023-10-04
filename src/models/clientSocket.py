import socket
import threading
import time


class ClientSocket:
    def __init__(self, dest_ip: str, protocol=socket.SOCK_DGRAM, disconnect_function: callable = None):
        self.socket = socket.socket(socket.AF_INET, protocol)
        self.protocol = protocol
        self.dest_ip = dest_ip
        self.disconnect_function = disconnect_function
        self.closed = False
        self.connect_socket()

    def start(self):
        self.thread_receiver = threading.Thread(
            target=self._start_receive, args=(), daemon=True)
        self.thread_receiver.start()
        time.sleep(1)

    def connect_socket(self):
        source_port = self.socket.getsockname()[1]
        source_ip = self.socket.getsockname()[0]
        self.socket.bind((source_ip, source_port))

    def send_package(self, data: str, dest_port: int):
        if not self.closed:
            package = data.encode("utf-8")
            self.socket.sendto(package, (self.dest_ip, dest_port))

    def close_socket(self):
        self.closed = True
        return self.socket.close()

    def _open_package(self, package: tuple) -> str:
        data = package[0].decode("utf-8")
        return data

    def _start_receive(self):
        port = self.socket.getsockname()[1]
        while True:
            print(f"Client is receiving messages on port {port}")
            data = self._open_package(self.socket.recvfrom(1024))
            if '/exit' in data:
                self.close_socket()
                self.disconnect_function(-2)
            elif '/disconnect' in data:
                self.close_socket()
                self.disconnect_function(-3)

            else:
                print(f"Nova mensagem de {data}")
