import threading
import time
from typing import List
from models.commands_enum import CommandsEnum
from models.client import Client
from models.message import Command
from models.serverSocket import ServerSocket


class Chat:
    def __init__(self, data_server: ServerSocket, control_server: ServerSocket):
        self.data_server = data_server
        self.control_server = control_server
        self.data_message: Command = None
        self.control_message: Command = None
        # Dicionário para guardar clientes conectados
        self.clients: List[Client] = []

    def start(self):
        thread_data = threading.Thread(
            target=self._thread_data_start, args=(), daemon=True)
        thread_control = threading.Thread(
            target=self._thread_control_start, args=(), daemon=True)
        thread_data.start()
        thread_control.start()
        while True:
            try:

                if self.control_message is not None:
                    self.handle_control(self.control_message)
                    self.control_message = None
                if self.data_message is not None:
                    self.handle_data(self.data_message)
                    self.data_message = None
                # print("Chat is waiting for new packages..")
                time.sleep(1)
            except KeyboardInterrupt:
                self.control_server.stop_server()
                self.data_server.stop_server()
                return
            # if command == None:
            #     print("Chat Server is shutting down...")
            #     self.server_socket.stop_server()
            #     break
            # Verifica se os dados são do controle ou do protocolo de dados
            # if not command.command in [CommandsEnum.CONNECT.value, CommandsEnum.EXIT.value]:
            #     self.handle_data(command)
            # else:
            #     self.handle_control(command)

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

    def _thread_data_start(self):
        port = self.data_server.port
        while True:
            try:
                if self.data_message is None:
                    print(f"Listening on port {port}")
                    self.data_message = self.data_server.receive_package()
                else:
                    time.sleep(0.2)
            except KeyboardInterrupt:
                self.data_server.stop_server()
                return

    def _thread_control_start(self):
        port = self.control_server.port
        while True:
            if self.control_message is None:
                print(f"Listening on port {port}")
                self.control_message = self.control_server.receive_package()
            else:
                time.sleep(0.2)
