from socket import SOCK_DGRAM
from models.chat import Chat
from models.serverSocket import ServerSocket

CONFIG = {
    "MAC_ORIGEM": "00:22:48:4d:10:e9",    # Substituir pelos endereços MAC desejados
    "MAC_DESTINO": "00:d7:6d:65:b5:3f",
    "IP_ORIGEM": "127.0.0.1",            # Substituir pelos endereços IP desejados
    "IP_DESTINO": "127.0.0.1",
    "PORTA_DADOS": 12345,
    "PORTA_CONTROLE": 12346,
    # Substituir pelo nome da interface de rede da máquina
    "INTERFACE_REDE": "lo"
}


def main():
    server = ServerSocket(source_ip=CONFIG["IP_ORIGEM"],
                          data_port=CONFIG["PORTA_DADOS"],
                          control_port=CONFIG["PORTA_CONTROLE"],
                          # passando UDP socket type
                          protocol=SOCK_DGRAM
                          )

    chat = Chat(server_socket=server)
    chat.start()


if __name__ == "__main__":
    main()
