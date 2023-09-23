import socket
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

    def bind_server(self, source_ip, data_port, control_port):
        self.socket_data.bind((source_ip, data_port))
        self.socket_control.bind((source_ip, control_port))
        self.data_port = data_port
        self.control_port = control_port

    def receive_package(self) -> Command:
        print(
            f"""Server's up! Listening on ports: 
                {self.data_port} for data messages
                {self.control_port} for control messages""")
        while True:
            try:
                # TODO
                # criar uma thread para cada Socket, um controle e um dados
                # Threads vao retornar as novas mensagens para o chat
                data_pkt = self.socket_data.recvfrom(65535)
                # control_pkt = self.socket_control.recvfrom(65535)
                # print(data_pkt)
                new_message = self._open_package(package=data_pkt)

                return new_message
            except KeyboardInterrupt:
                return None
            except Exception as e:
                print(f"Erro ao receber pacote UDP: {e}")
                return None

    def stop_server(self):
        self.socket_data.close()
        self.socket_control.close()
        return

    def _open_package(self, package: tuple) -> Command:
        data = package[0].decode("utf-8")
        ip = package[1][0]
        port = package[1][1]
        return Command(source_ip=ip, source_port=port, data=data)
