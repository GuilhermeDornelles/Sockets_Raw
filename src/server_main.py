from socket import SOCK_DGRAM, SOCK_STREAM
from models.chat import Chat, ChatTCP
from models.serverSocket import ServerSocketTCP, ServerSocketUDP

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
# SOCKET_PROTOCOL = SOCK_DGRAM
SOCKET_PROTOCOL = SOCK_STREAM


def main():
    if SOCKET_PROTOCOL == SOCK_STREAM:
        data_server = ServerSocketTCP(source_ip=CONFIG["IP_ORIGEM"],
                                      port=CONFIG["PORTA_DADOS"],
                                      # passando UDP socket type
                                      protocol=SOCKET_PROTOCOL
                                      )
        control_server = ServerSocketTCP(source_ip=CONFIG["IP_ORIGEM"],
                                         port=CONFIG["PORTA_CONTROLE"],
                                         # passando UDP socket type
                                         protocol=SOCKET_PROTOCOL
                                         )
        chat = ChatTCP(data_server=data_server, control_server=control_server)

    elif SOCKET_PROTOCOL == SOCK_DGRAM:
        data_server = ServerSocketUDP(source_ip=CONFIG["IP_ORIGEM"],
                                      port=CONFIG["PORTA_DADOS"],
                                      # passando UDP socket type
                                      protocol=SOCK_DGRAM
                                      )
        control_server = ServerSocketUDP(source_ip=CONFIG["IP_ORIGEM"],
                                         port=CONFIG["PORTA_CONTROLE"],
                                         # passando UDP socket type
                                         protocol=SOCK_DGRAM
                                         )

        chat = Chat(data_server=data_server, control_server=control_server)

    chat.start()


if __name__ == "__main__":
    main()
