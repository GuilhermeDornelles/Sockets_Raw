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
        # Manda para um cliente específico
        if command.command == CommandsEnum.PRIVMSG.value:
            # TODO command precisa ter referencia para o destino da mensagem (name)
            client = self._find_client_from_name(name=command.dest)
            # TODO trocar command.options[1] para command.text
            if (self.data_server.send_package(command.options[1], client)):
                print(f"Mensagem enviada para o {client}")
            else:
                print(f"Erro ao enviar mensagem para {client}")
        # Manda para todos os clientes conectados
        elif command.command == CommandsEnum.MSG.value:
            error = False
            for client in self.clients:
                if not (self.data_server.send_package(command.options[0], client)):
                    error = True
            if not error:
                print(f"Mensagem enviada para todos os clients.")
            else:
                print(f"Erro ao enviar mensagem para todos os clients.")

    def handle_control(self, command: Command):
        if command.command == CommandsEnum.CONNECT.value:
            new_client = Client(ip=command.source_ip,
                                port=command.source_port,
                                name=command.options[0])
            if (self.add_client(new_client)):
                print("Cliente registrado com sucesso")
            else:
                print("Nome ou porta de cliente em uso!")
        elif command.command in CommandsEnum.EXIT.value:
            client = self._find_client_from_command(command)
            if (self.remove_client(client)):
                print(f"Cliente {client} com sucesso")
            else:
                print("Cliente não encontrado!")

    def add_client(self, client) -> bool:
        for clt in self.clients:
            if clt.name == client.name or clt.port == client.port:
                return False

        self.clients.append(client)
        return True

    def remove_client(self, client):
        try:
            self.clients.remove(client)
            return True
        except ValueError:
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

    def _find_client_from_command(self, command: Command) -> Client:
        return next(filter(lambda c: c.port ==
                           command.source_port, self.clients), None)

    def _find_client_from_name(self, name: str) -> Client:
        return next(filter(lambda c: c.name ==
                           name, self.clients), None)
