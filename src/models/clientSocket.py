import socket
import threading
import time
from abc import ABC, abstractmethod


class ClientSocket(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def connect_socket(self):
        pass

    @abstractmethod
    def send_package(self, data: str, dest_port: int):
        pass

    @abstractmethod
    def close_socket(self):
        pass

    @abstractmethod
    def _open_package(self, package: tuple) -> str:
        pass

    @abstractmethod
    def _create_file(self, filename: str, content: str) -> bool:
        pass

    @abstractmethod
    def _start_receive(self):
        pass


class ClientSocketUDP(ClientSocket):
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
        if self.closed:
            return
        if "file" in data.split()[0]:
            try:
                readByte = open(data.split()[-1], "rb")
                file_b = readByte.read()
                readByte.close()
                package = (data + " ").encode("utf-8") + file_b
            except FileNotFoundError:
                print("Arquivo nao encontrado, nao foi possivel enviar o pacote.")
                return
        else:
            package = data.encode("utf-8")

        self.socket.sendto(package, (self.dest_ip, dest_port))

    def close_socket(self):
        self.closed = True
        return self.socket.close()

    def _open_package(self, package: tuple) -> str:
        return package[0].decode("utf-8")

    def _create_file(self, filename: str, content: str) -> bool:
        try:
            with open(filename, "w") as file:
                file.write(content)
            return True
        except Exception:
            return False

    def _start_receive(self):
        port = self.socket.getsockname()[1]
        while True:
            print(f"Client is receiving messages on port {port}")
            data = self._open_package(self.socket.recvfrom(1024))
            parts = data.split(" ")
            if '/exit' in data:
                self.close_socket()
                self.disconnect_function(-2)
            elif '/disconnect' in data:
                self.close_socket()
                self.disconnect_function(-3)
            elif '/file' in parts[0]:
                filename = parts[1]
                f_created = self._create_file(
                    filename, content=data.lstrip("/file " + filename))
                if f_created:
                    print("Arquivo criado com sucesso.")
                else:
                    print("Erro ao criar arquivo com connteúdo.")

            else:
                print(f"Nova mensagem de {data}")


class ClientSocketTCP(ClientSocket):
    def __init__(self, dest_ip: str, dest_port: int = None, protocol=socket.SOCK_DGRAM, disconnect_function: callable = None):
        self.socket = socket.socket(socket.AF_INET, protocol)
        self.protocol = protocol
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.disconnect_function = disconnect_function
        self.closed = False
        self.connected = False
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
        # self.socket.listen(1)
        # self.socket.connect((self.dest_ip, self.dest_port))

    def send_package(self, data: str, dest_port: int):
        if self.closed:
            return
        if "file" in data.split()[0]:
            try:
                readByte = open(data.split()[-1], "rb")
                file_b = readByte.read()
                readByte.close()
                package = (data + " ").encode("utf-8") + file_b
            except FileNotFoundError:
                print("Arquivo nao encontrado, nao foi possivel enviar o pacote.")
                return
        else:
            package = data.encode("utf-8")
        if not self.connected:
            self.socket.connect((self.dest_ip, self.dest_port))
            self.connected = True
        self.socket.sendall(package)

        # self.socket.sendto(package, (self.dest_ip, dest_port))

    def close_socket(self):
        self.closed = True
        return self.socket.close()

    def _open_package(self, package: tuple) -> str:
        return package.decode("utf-8")

    def _create_file(self, filename: str, content: str) -> bool:
        try:
            with open(filename, "w") as file:
                file.write(content)
            return True
        except Exception:
            return False

    def _start_receive(self):
        port = self.socket.getsockname()[1]
        while True:
            print(f"Client is receiving messages on port {port}")

            temp_socket = socket.socket(socket.AF_INET, self.protocol)
            temp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            source_port = self.socket.getsockname()[1]
            source_ip = self.socket.getsockname()[0]
            temp_socket.bind((source_ip, (source_port+1)))
            temp_socket.listen(1)
            connection, _addr = temp_socket.accept()
            package = connection.recv(1024)
            data = self._open_package(package)
            connection.close()

            if data == "":
                break
            parts = data.split(" ")
            if '/exit' in data:
                self.close_socket()
                self.disconnect_function(-2)
            elif '/disconnect' in data:
                self.close_socket()
                self.disconnect_function(-3)
            elif '/file' in parts[0]:
                filename = parts[1]
                f_created = self._create_file(
                    filename, content=data.lstrip("/file " + filename))
                if f_created:
                    print("Arquivo criado com sucesso.")
                else:
                    print("Erro ao criar arquivo com conteúdo.")

            else:
                print(f"Nova mensagem de {data}")
