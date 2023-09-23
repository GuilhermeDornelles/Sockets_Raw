from socket import SOCK_DGRAM
from models.clientSocket import ClientSocket

CONFIG = {
    "MAC_ORIGEM": "00:22:48:4d:10:e9",     # Substituir pelos endereços MAC desejados
    "MAC_DESTINO": "00:d7:6d:65:b5:3f",
    # "IP_ORIGEM": "192.168.0.180",
    # "IP_DESTINO": "192.168.0.180",         # Substituir pelos endereços IP desejados
    "IP_ORIGEM": "127.0.0.1",
    "IP_DESTINO": "127.0.0.1",         # Substituir pelos endereços IP desejados
    "PORTA_ORIGEM": 61,
    "PORTA_DESTINO": 12345,
    # Substituir pelo nome da interface de rede da máquina
    "INTERFACE_REDE": "lo"
}


def main():
    socket = ClientSocket(dest_ip=CONFIG["IP_DESTINO"],
                          dest_port=CONFIG["PORTA_DESTINO"],
                          protocol=SOCK_DGRAM
                          #   source_port=CONFIG["PORTA_ORIGEM"],
                          #   net_interface=CONFIG["INTERFACE_REDE"],
                          )

    socket.send_package(data="Isto eh um teste")
    socket.send_package(data="Teste dois !")


if __name__ == "__main__":
    main()
