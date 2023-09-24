import socket
import threading
import time
from models.message import Command
from utils import format_and_validate_ip


class ServerSocket:
    # TODO
    # Tornar os atributos de endereços necessários conforme a implementação avançar
    def __init__(self, protocol, data_port=12345, control_port=12346, source_ip=""):
        self.socket_data = socket.socket(socket.AF_INET, protocol)
        self.socket_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.protocol = protocol
        self.bind_server(source_ip, data_port, control_port)
        self.source_ip = format_and_validate_ip(source_ip)
        self.new_package = None

    def bind_server(self, source_ip, data_port, control_port):
        self.socket_data.bind((source_ip, data_port))
        self.socket_control.bind((source_ip, control_port))
        self.data_port = data_port
        self.control_port = control_port

    def receive_package(self) -> Command:
        # WIP
        # Threads vao salvar a nova mensagem em self.new_package para o chat
        try:
            thread_data = threading.Thread(
                target=self._socket_receive_pkg, args=(self.socket_data, "data"), daemon=True)
            thread_control = threading.Thread(
                target=self._socket_receive_pkg, args=(self.socket_control, "control"), daemon=True)
            thread_data.start()
            thread_control.start()
            while thread_data.is_alive() and thread_control.is_alive():
                time.sleep(1)

            print("Enviou a mensagem para o chat")
            new_message = self._open_package(package=self.new_package)
            self.new_package = None
            return new_message
        except KeyboardInterrupt:
            return None
        # except Exception as e:
        #     print(f"Erro ao receber pacote UDP: {e}")
        #     return None

    def stop_server(self):
        self.socket_data.close()
        self.socket_control.close()
        return

    def _open_package(self, package: tuple) -> Command:
        data = package[0].decode("utf-8")
        ip = package[1][0]
        port = package[1][1]
        return Command(source_ip=ip, source_port=port, data=data)

    def _socket_receive_pkg(self, sckt: socket, msg_type):
        port = sckt.getsockname()[1]
        # if self.new_package is None:
        print(f"Thread for Server starting in port {port} for {msg_type}")
        self.new_package = sckt.recvfrom(1024)
        print(f"New package saved by thread {msg_type}.")
