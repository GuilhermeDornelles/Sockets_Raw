from models.serverSocket import ServerSocket
from socket import IPPROTO_UDP

CONFIG = {
    "MAC_ORIGEM": "00:22:48:4d:10:e9",    # Substituir pelos endereços MAC desejados
    "MAC_DESTINO": "00:d7:6d:65:b5:3f",
    "IP_ORIGEM": "192.168.0.180",            # Substituir pelos endereços IP desejados
    "IP_DESTINO": "192.168.0.180",
    "PORTA_ORIGEM": 12345,
    "PORTA_DESTINO": 61,
    # Substituir pelo nome da interface de rede da máquina
    "INTERFACE_REDE": "eth0"
}


def main():
    server = ServerSocket(source_mac=CONFIG["MAC_ORIGEM"],
                          dest_mac=CONFIG["MAC_DESTINO"],
                          source_ip=CONFIG["IP_ORIGEM"],
                          dest_ip=CONFIG["IP_DESTINO"],
                          source_port=CONFIG["PORTA_ORIGEM"],
                          dest_port=CONFIG["PORTA_DESTINO"],
                          net_interface=CONFIG["INTERFACE_REDE"],
                          protocol=IPPROTO_UDP
                          )

    server.run_server()


if __name__ == "__main__":
    main()
