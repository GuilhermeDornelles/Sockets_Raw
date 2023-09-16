from socket import IPPROTO_UDP
from models.clientSocket import ClientSocket

CONFIG = {
    "MAC_ORIGEM": "00:22:48:4d:10:e9",     # Substituir pelos endereços MAC desejados
    "MAC_DESTINO": "00:d7:6d:65:b5:3f",
    "IP_ORIGEM": "192.168.0.180",
    "IP_DESTINO": "192.168.0.180",         # Substituir pelos endereços IP desejados
    "PORTA_ORIGEM": 61,
    "PORTA_DESTINO": 12345,
    # Substituir pelo nome da interface de rede da máquina
    "INTERFACE_REDE": "eth0"
}


def main():
    socket = ClientSocket(source_mac=CONFIG["MAC_ORIGEM"],
                          dest_mac=CONFIG["MAC_DESTINO"],
                          source_ip=CONFIG["IP_ORIGEM"],
                          dest_ip=CONFIG["IP_DESTINO"],
                          source_port=CONFIG["PORTA_ORIGEM"],
                          dest_port=CONFIG["PORTA_DESTINO"],
                          net_interface=CONFIG["INTERFACE_REDE"],
                          protocol=IPPROTO_UDP
                          )

    socket.send_package(data="mensagem de teste")


if __name__ == "__main__":
    main()
