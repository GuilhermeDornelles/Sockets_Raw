from models.message import Command
from models.serverSocket import ServerSocket


class Chat:
    EXIT_COMMAND = "/EXIT"
    CONNECT_COMMAND = "/CONNECT"
    PRIVMSG_COMMAND = "/PRIVMSG"
    MSG_COMMAND = "/MSG"

    def __init__(self, server_socket: ServerSocket):
        self.server_socket = server_socket
        self.clients = {}  # Dicionário para guardar clientes conectados

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
            # if not command.command.upper() in [CONNECT_COMMAND, EXIT_COMMAND]:
            #     # Tratar dados do cliente
            #     self.handle_data(command)
            # else:
            #     # Tratar dados de controle (novas conexões, desconexões, etc.)
            #     self.handle_control(command)

    def handle_data(self, command: Command):
        # TODO
        # testar ver se esta recebendo a mensagem de maneira correta
        print(f"Received from {command.source_port}: {command.command}")

        # Exemplo de como mandar a mensagem para os outros clientes
        # for client_addr in self.clients:
        #     if client_addr != addr:
        #         self.server_socket.sendto(data, client_addr)

    def handle_control(self, command: Command):
        # TODO
        # Melhorar e falar com o grupo sobre implementação
        # Adicionar e remover clientes
        print(f"Received from {command.source_port}: {command.command}")
        # if data == "connect":
        #     self.add_client(addr)
        # elif data == 'exit':
        #     self.remove_client(addr)

    def add_client(self, addr):
        self.clients[addr] = None

    def remove_client(self, addr):
        del self.clients[addr]
