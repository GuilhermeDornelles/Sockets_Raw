import threading
import time
from typing import List
from models.commands_enum import CommandsEnum
from models.client import Client
from models.command import Command
from models.serverSocket import ServerSocket
from utils import super_print
EXIT_COMMAND = '/exit'
DISCONNECT_COMMAND = '/disconnect'


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
                if len(self.clients) > 0:
                    self.disconnect_all_clients()
                self.control_server.stop_server()
                self.data_server.stop_server()
                return

    def handle_data(self, command: Command):
        # Manda para um cliente específico
        if command.type == CommandsEnum.PRIVMSG.value:
            source_client = self._find_client_from_command(command=command)
            pack = f"{source_client.name}: {command.data}"
            self._send_unicast_data(package=pack, command=command)
        elif command.type == CommandsEnum.PRIVFILE.value:
            pack = f"/file {command.file_path} {command.data}"
            self._send_unicast_data(package=pack, command=command)
        # Manda para todos os clientes conectados
        elif command.type == CommandsEnum.MSG.value:
            source_client = self._find_client_from_command(command=command)
            pack = f"{source_client.name}: {command.data}"
            self._send_broadcast_data(package=pack, command=command)
        elif command.type == CommandsEnum.FILE.value:
            pack = f"/file {command.file_path} {command.data}"
            self._send_broadcast_data(package=pack, command=command)

    def _send_unicast_data(self, package, command):
        dest_client = self._find_client_from_name(name=command.dest_name)
        if (self.data_server.send_package(package, dest_client)):
            print(f"Mensagem enviada para o {dest_client}")
        else:
            print(f"Erro ao enviar mensagem para {dest_client}")

    def _send_broadcast_data(self, package, command):
        error = False
        for dest_client in self.clients:
            if dest_client.port != command.source_port and not (self.data_server.send_package(package, dest_client)):
                error = True
        if not error:
            print("Mensagem enviada para todos os clients.")
        else:
            print("Erro ao enviar mensagem para todos os clients.")

    def handle_control(self, command: Command):
        if command.type == CommandsEnum.CONNECT.value:
            new_client = Client(ip=command.source_ip,
                                port=command.source_port,
                                name=command.data)
            if (self.add_client(new_client)):
                print(f"Cliente {new_client} registrado com sucesso")
                print(f"\n{self.clients}\n")
            else:
                print("Nome ou porta de cliente em uso!")
                self._disconnect_client(new_client)

        elif command.type in CommandsEnum.EXIT.value:
            client = self._find_client_from_command(command)
            if (self.remove_client(client)):
                print(f"Cliente {client} com sucesso")
                print(f"\n{self.clients}\n")
            else:
                print("Cliente não encontrado!")

    def add_client(self, client: Client) -> bool:
        for clt in self.clients:
            if clt.name == client.name or clt.port == client.port:
                return False

        self.clients.append(client)
        return True

    def _disconnect_client(self, client: Client, command: str = ''):
        self.data_server.send_package(command, client)
        return True

    def remove_client(self, client: Client):
        try:
            self.clients.remove(client)
            self._disconnect_client(client, EXIT_COMMAND)
            return True
        except ValueError:
            return False

    def disconnect_all_clients(self):
        super_print("Desconectando todos os clientes")
        for client in self.clients:
            self._disconnect_client(client, EXIT_COMMAND)
        super_print("Todos clientes desconectados")
        return True

    def _validate_and_handle(self, handle_func: callable, command: Command):
        if Command.type_is_valid(command):
            handle_func(command)
        else:
            print(f"Command not valid: {command.type}")

    def _thread_data_start(self):
        port = self.data_server.port
        while True:
            if self.data_message is None:
                print(f"Listening on port {port}")
                self.data_message = self.data_server.receive_package()
                if self.data_message is not None:
                    print(f"Received message: {self.data_message}")
            else:
                time.sleep(0.2)

    def _thread_control_start(self):
        port = self.control_server.port
        while True:
            if self.control_message is None:
                print(f"Listening on port {port}")
                self.control_message = self.control_server.receive_package()
                if self.control_message is not None:
                    print(f"Received message: {self.control_message}")
            else:
                time.sleep(0.2)

    def _find_client_from_command(self, command: Command) -> Client:
        return next(filter(lambda c: c.port ==
                           command.source_port, self.clients), None)

    def _find_client_from_name(self, name: str) -> Client:
        return next(filter(lambda c: c.name ==
                           name, self.clients), None)


class ChatTCP:
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
        thread_data.start()
        while True:
            try:
                if len(self.data_server.messages) > 0:
                    print(self.data_server.messages)
                    message = self.data_server.messages[0]
                    self._validate_and_handle(
                        handle_func=self.handle_data, command=message)
                    self.data_server.messages.remove(message)
                time.sleep(1)
            except KeyboardInterrupt:
                if len(self.clients) > 0:
                    self.disconnect_all_clients()
                self.control_server.stop_server()
                self.data_server.stop_server()
                return

    def handle_data(self, command: Command):
        # Manda para um cliente específico
        if command.type == CommandsEnum.PRIVMSG.value:
            source_client = self._find_client_from_command(command=command)
            pack = f"{source_client.name}: {command.data}"
            self._send_unicast_data(package=pack, command=command)
        elif command.type == CommandsEnum.PRIVFILE.value:
            pack = f"/file {command.file_path} {command.data}"
            self._send_unicast_data(package=pack, command=command)
        # Manda para todos os clientes conectados
        elif command.type == CommandsEnum.MSG.value:
            source_client = self._find_client_from_command(command=command)
            pack = f"{source_client.name}: {command.data}"
            self._send_broadcast_data(package=pack, command=command)
        elif command.type == CommandsEnum.FILE.value:
            pack = f"/file {command.file_path} {command.data}"
            self._send_broadcast_data(package=pack, command=command)
        else:
            self.handle_control(command=command)

    def handle_control(self, command: Command):
        if command.type == CommandsEnum.CONNECT.value:
            new_client = Client(ip=command.source_ip,
                                port=command.source_port,
                                name=command.data)
            if (self.add_client(new_client)):
                print(f"Cliente {new_client} registrado com sucesso")
                print(f"\n{self.clients}\n")
            else:
                print("Nome ou porta de cliente em uso!")
                self._disconnect_client(new_client)

        elif command.type in CommandsEnum.EXIT.value:
            client = self._find_client_from_command(command)
            if (self.remove_client(client)):
                print(f"Cliente {client} com sucesso")
                print(f"\n{self.clients}\n")
            else:
                print("Cliente não encontrado!")

    def _send_unicast_data(self, package, command):
        dest_client = self._find_client_from_name(name=command.dest_name)
        if (self.data_server.send_package(package, dest_client)):
            print(f"Mensagem enviada para o {dest_client}")
        else:
            print(f"Erro ao enviar mensagem para {dest_client}")

    def _send_broadcast_data(self, package, command):
        error = False
        for dest_client in self.clients:
            if dest_client.port != command.source_port and not (self.data_server.send_package(package, dest_client)):
                error = True
        if not error:
            print("Mensagem enviada para todos os clients.")
        else:
            print("Erro ao enviar mensagem para todos os clients.")

    def add_client(self, client: Client) -> bool:
        for clt in self.clients:
            if clt.name == client.name or clt.port == client.port:
                return False

        self.clients.append(client)
        return True

    def _disconnect_client(self, client: Client, command: str = ''):
        self.data_server.send_package(command, client)
        return True

    def remove_client(self, client: Client):
        try:
            self.clients.remove(client)
            self._disconnect_client(client, EXIT_COMMAND)
            return True
        except ValueError:
            return False

    def disconnect_all_clients(self):
        super_print("Desconectando todos os clientes")
        for client in self.clients:
            self._disconnect_client(client, EXIT_COMMAND)
        super_print("Todos clientes desconectados")
        return True

    def _validate_and_handle(self, handle_func: callable, command: Command):
        if Command.type_is_valid(command):
            handle_func(command)
        else:
            print(f"Command not valid: {command.type}")

    def _thread_data_start(self):
        port = self.data_server.port
        while True:
            if self.data_message is None:
                print(f"Listening on port {port}")
                self.data_message = self.data_server.connect_clients()
                if self.data_message is not None:
                    print(f"Received message: {self.data_message}")
            else:
                time.sleep(0.2)

    def _thread_control_start(self):
        port = self.control_server.port
        while True:
            if self.control_message is None:
                print(f"Listening on port {port}")
                self.control_message = self.control_server.connect_clients()
                if self.control_message is not None:
                    print(f"Received message: {self.control_message}")
            else:
                time.sleep(0.2)

    def _find_client_from_command(self, command: Command) -> Client:
        return next(filter(lambda c: c.port ==
                           command.source_port, self.clients), None)

    def _find_client_from_name(self, name: str) -> Client:
        return next(filter(lambda c: c.name ==
                           name, self.clients), None)
