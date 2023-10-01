import threading
import time
from typing import List
from models.commands_enum import CommandsEnum
from models.client import Client
from models.command import Command
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
                    self._validate_and_handle(
                        handle_func=self.handle_control, command=self.control_message)
                    self.control_message = None
                if self.data_message is not None:
                    self._validate_and_handle(
                        handle_func=self.handle_data, command=self.data_message)
                    self.data_message = None
                time.sleep(1)
            except KeyboardInterrupt:
                self.control_server.stop_server()
                self.data_server.stop_server()
                return

    def handle_data(self, command: Command):
        # TODO
        # testar ver se esta recebendo a mensagem de maneira correta
        print(f"Received data from {command.source_port}: {command.command}")

        # Manda para um cliente específico
        if command.command == CommandsEnum.PRIVMSG.value:
            # TODO => Como pegar a porta
            self.data_server.sendto(self.data_message, '')
        # Manda para todos os clientes conectados
        elif command.command == CommandsEnum.MSG.value:
            for client_addr in self.clients:
                if client_addr != command.addr:
                    self.data_server.sendto(self.data_message, client_addr)

    def handle_control(self, command: Command):
        print(
            f"Received control from {command.source_port}: {command.command}")
        if command.command == CommandsEnum.CONNECT.value:
            if (self.add_client()):  # TODO -> Como passar as informações do cliente
                print("Cliente registrado com sucesso")
            else:
                print("Nome ou porta de cliente em uso!")
        elif command.command is CommandsEnum.EXIT.value:
            if (self.remove_client()):  # TODO -> Como passar as informações do cliente
                print("Cliente removido com sucesso")
            else:
                print("Cliente não encontrado!")

        # return

    def add_client(self, client) -> bool:
        for clt in self.clients:
            if clt.name == client.name or clt.port == client.port:
                return False

        self.clients.append(client)
        return True

    def remove_client(self, client):
        for clt in self.clients:
            if clt == client:
                self.clients.remove(client)
                return True

        return False

    def _validate_and_handle(self, handle_func: callable, command: Command):
        if Command.command_is_valid(command) and Command.validate_command_options(command):
            handle_func(command)
        else:
            print(
                f"Command not valid: {command.command}")

    def _thread_data_start(self):
        port = self.data_server.port
        while True:
            if self.data_message is None:
                print(f"Listening on port {port}")
                self.data_message = self.data_server.receive_package()
            else:
                time.sleep(0.2)

    def _thread_control_start(self):
        port = self.control_server.port
        while True:
            if self.control_message is None:
                print(f"Listening on port {port}")
                self.control_message = self.control_server.receive_package()
            else:
                time.sleep(0.2)
