from socket import SOCK_DGRAM, SOCK_STREAM
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
    try:
        # UDP
        data_server = ServerSocket(
            source_ip=CONFIG["IP_ORIGEM"], port=CONFIG["PORTA_DADOS"], protocol=SOCK_DGRAM)
        control_server = ServerSocket(
            source_ip=CONFIG["IP_ORIGEM"], port=CONFIG["PORTA_CONTROLE"], protocol=SOCK_DGRAM)

        # TCP
        # data_server = ServerSocket(
        #     source_ip=CONFIG["IP_ORIGEM"], port=CONFIG["PORTA_DADOS"], protocol=SOCK_STREAM)
        # control_server = ServerSocket(
        #     source_ip=CONFIG["IP_ORIGEM"], port=CONFIG["PORTA_CONTROLE"], protocol=SOCK_STREAM)

        chat = Chat(data_server=data_server, control_server=control_server)
        chat.start()
    except KeyboardInterrupt:
        data_server.stop_server()
        control_server.stop_server()
    return True


if __name__ == "__main__":
    main()
