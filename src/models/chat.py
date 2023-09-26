from typing import List
from models.client import Client
from models.message import Command
from models.serverSocket import ChatServerSocket, ControlServerSocket

class Chat:
    def __init__(self, chat_socket: ChatServerSocket, control_socket: ControlServerSocket):
        self.chat_socket = chat_socket
        self.control_socket = control_socket
        # Dicionário para guardar clientes conectados
        self.clients: List[Client] = []

    def start(self):
        while True:
            # Recebe dados do socket 1024 é o tamanho do que vai receber(tamanho maximo)
            chat_command = self.chat_socket.receive_package()
            control_command = self.control_socket.receive_package()
            print("chat esta ouvindo..")
            if chat_command == None:
                print("Chat Server is shutting down...")
                self.chat_socket.stop_server()
                break
            if control_command == None:
                print("Chat Server is shutting down...")
                self.control_socket.stop_server()
                break
            # print(command)
            # Verifica se os dados são do controle ou do protocolo de dados
            if chat_command is not None:
                self.handle_data(chat_command)

            if control_command is not None:
                self.handle_control(control_command)

    def handle_data(self, command: Command):
        # TODO
        # testar ver se esta recebendo a mensagem de maneira correta
        print(f"Received data from {command.source_port}: {command.command}")

        # Exemplo de como mandar a mensagem para os outros clientes
        # for client_addr in self.clients:
        #     if client_addr != addr:
        #         self.server_socket.sendto(data, client_addr)

    def handle_control(self, command: Command):
        print(
            f"Received control from {command.source_port}: {command.command}")
        # TODO
        # Melhorar e falar com o grupo sobre implementação
        # Adicionar e remover clientes
        # if data == "connect":
        #     self.add_client(addr)
        # elif data == 'exit':
        #     self.remove_client(addr)

    def add_client(self, client):
        # TODO logica p verificar se cliente com aquele nome / porta ja n esta conectado
        self.clients.append(client)

    def remove_client(self, client):
        # TODO logica p verificar se cliente com aquele nome / porta esta conectado
        self.clients.remove(client)
