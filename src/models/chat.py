from client import Client
from models.message import Command
from models.serverSocket import ServerSocket


class Chat:
    EXIT_COMMAND = "/EXIT"
    CONNECT_COMMAND = "/CONNECT"
    PRIVMSG_COMMAND = "/PRIVMSG"
    MSG_COMMAND = "/MSG"

    def __init__(self, server_socket: ServerSocket):
        self.server_socket = server_socket
        # Dicionário para guardar clientes conectados
        self.clients = list(Client)

    def start(self):
        while True:
            # Recebe dados do socket 1024 é o tamanho do que vai receber(tamanho maximo)
            command = self.server_socket.receive_package()
            if command == None:
                print("Chat Server is shutting down...")
                self.server_socket.stop_server()
                break
            print(command)
            # Verifica se os dados são do controle ou do protocolo de dados
            if not command.command.upper() in [self.CONNECT_COMMAND, self.EXIT_COMMAND]:
                # Tratar dados do cliente
                self.handle_data(command)
            else:
                # Tratar dados de controle (novas conexões, desconexões, etc.)
                self.handle_control(command)

    def handle_data(self, command: Command):
        # TODO
        # testar ver se esta recebendo a mensagem de maneira correta
        print(f"Received from {command.source_port}: {command.command}")

        # Exemplo de como mandar a mensagem para os outros clientes
        # for client_addr in self.clients:
        #     if client_addr != addr:
        #         self.server_socket.sendto(data, client_addr)

    def handle_control(self, command: Command):
        print(f"Received from {command.source_port}: {command.command}")
        # TODO
        # Melhorar e falar com o grupo sobre implementação
        # Adicionar e remover clientes
        # if data == "connect":
        #     self.add_client(addr)
        # elif data == 'exit':
        #     self.remove_client(addr)

    def add_client(self, client):
        # TODO
        # logica p verificar se cliente com aquele nome / porta ja n esta conectado
        self.clients.append(client)

    def remove_client(self, client):
        # TODO
        # logica p verificar se cliente com aquele nome / porta esta conectado
        self.clients.remove(client)
