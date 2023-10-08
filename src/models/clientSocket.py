from socket import SOCK_DGRAM, SOCK_STREAM
import socket


class ClientSocket:
    def __init__(self, dest_ip: str, protocol=socket.SOCK_DGRAM, disconnect_function: callable = None):
        self.socket = socket.socket(socket.AF_INET, protocol)
        self.protocol = protocol
        self.dest_ip = dest_ip
        self.disconnect_function = disconnect_function
        self.closed = False
        self.connect_socket()

    def start(self):
        # self.thread_receiver = threading.Thread(
        #     target=self._start_receive, args=(), daemon=True)
        # self.thread_receiver.start()
        # time.sleep(1)
        pass

    def connect_socket(self):
        # source_port = self.socket.getsockname()[1]
        # source_ip = self.socket.getsockname()[0]
        # self.socket.bind((source_ip, source_port))
        # print("bind()")
        # self.socket.listen(1)
        print("listen()")

    def send_package(self, data: str, dest_port: int):
<<<<<<< HEAD
        try:
            if self.closed:
                return
            if "file" in data.split()[0]:
                try:
                    read_byte = open(data.split()[-1], "rb")
                    file_b = read_byte.read()
                    read_byte.close()
                    package = (data + " ").encode("utf-8") + file_b
                except FileNotFoundError:
                    print("Arquivo nao encontrado, nao foi possivel enviar o pacote.")
                    return
            else:
                package = data.encode("utf-8")

            if self.socket.type == SOCK_STREAM:
                self.socket.connect((self.dest_ip, dest_port))
                print("connect()")
                # self.socket.sendall(package)
                self.socket.sendto(package, (self.dest_ip, dest_port))
                print("sendto()")
            else:
                self.socket.sendto(package, (self.dest_ip, dest_port))
        except Exception as e:
            print(e)
=======
        if not self.closed:
            package = data.encode("utf-8")
            self.socket.sendto(package, (self.dest_ip, dest_port))
>>>>>>> parent of de74f73 (fechando o pastel do UDP)

    def close_socket(self):
        self.closed = True
        return self.socket.close()

<<<<<<< HEAD
    def _open_package_udp(self, package: tuple) -> str:
        return package[0].decode("utf-8")

    def _open_package_tcp(self, package):
        return package.decode("utf-8")

    def _create_file(self, filename: str, content: str) -> bool:
        try:
            with open(filename, "w") as file:
                file.write(content)
            return True
        except Exception:
            return False
=======
    def _open_package(self, package: tuple) -> str:
        data = package[0].decode("utf-8")
        return data
>>>>>>> parent of de74f73 (fechando o pastel do UDP)

    def _start_receive(self):
        port = self.socket.getsockname()[1]
        while True:
            print(f"Client is receiving messages on port {port}")
<<<<<<< HEAD
            if self.socket.type == SOCK_DGRAM:
                data = self._open_package_udp(self.socket.recvfrom(1024))
=======
            data = self._open_package(self.socket.recvfrom(1024))
            if '/exit' in data:
                self.close_socket()
                self.disconnect_function(-2)
            elif '/disconnect' in data:
                self.close_socket()
                self.disconnect_function(-3)

>>>>>>> parent of de74f73 (fechando o pastel do UDP)
            else:
                connection, addr = self.socket.accept()
                package = connection.recv(1024)
                data = self._open_package_tcp(package)

            if data is not None:
                data = self._open_package(data)
                parts = data.split(" ")
                print(parts)
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
