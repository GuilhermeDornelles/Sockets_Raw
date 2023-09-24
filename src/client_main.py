from socket import SOCK_DGRAM
from models.clientSocket import ClientSocket

CONFIG = {
    "IP_ORIGEM": "127.0.0.1",
    "IP_DESTINO": "127.0.0.1",         # Substituir pelos endereços IP desejados
    "PORTA_ORIGEM": 61,
    "PORTA_DESTINO": 12345,
}


def main():
    socket = ClientSocket(dest_ip=CONFIG["IP_DESTINO"],
                          dest_port=CONFIG["PORTA_DESTINO"],
                          protocol=SOCK_DGRAM
                          #   source_port=CONFIG["PORTA_ORIGEM"],
                          #   net_interface=CONFIG["INTERFACE_REDE"],
                          )

    # socket.send_package(data="/CONNECT")
    socket.send_package(data="Qualquer coisa")
    socket.send_package(data="Teste dois !")


if __name__ == "__main__":
    main()
