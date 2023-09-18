class Chat:
    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.clients = {}  # Dicionário para guardar clientes conectados

    def start(self):
        while True:
            data, addr = self.server_socket.recvfrom(1024)  # Recebe dados do socket 1024 é o tamanho do que vai receber(tamanho maximo)

            # Verifica se os dados são do controle ou do protocolo de dados
            if addr in self.clients:
                # Tratar dados do cliente
                self.handle_data(data, addr)
            else:
                # Tratar dados de controle (novas conexões, desconexões, etc.)
                self.handle_control(data, addr)

    def handle_data(self, data, addr):
        #TODO
        message = data.decode("utf-8")
        print(f"Received from {addr}: {message}") # testar ver se esta recebendo a mensagem de maneira correta

        #Exemplo de como mandar a mensagem para os outros clientes
        for client_addr in self.clients:
            if client_addr != addr:
                self.server_socket.sendto(data, client_addr)

    def handle_control(self, data, addr):
        #TODO
        # Melhorar e falar com o grupo sobre implementação
        # Adicionar e remover clientes 
        if data == b'join':
            self.add_client(addr)
        elif data == b'leave':
            self.remove_client(addr)

    def add_client(self, addr):
        self.clients[addr] = None

    def remove_client(self, addr):
        del self.clients[addr]