from socket import SOCK_RAW
from serverSocket import ServerSocket

CONFIG = {
    # "MAC_ORIGEM": "a4:1f:72:f5:90:52",
    # "MAC_ORIGEM": "02:42:6c:83:f3:8e",
    "MAC_ORIGEM": "00:22:48:4d:10:e9",    # Substituir pelos endereços MAC desejados
    "MAC_DESTINO": "00:d7:6d:65:b5:3f",
    "IP_ORIGEM": "172.16.5.4",            # Substituir pelos endereços IP desejados
    "IP_DESTINO": "192.168.1.171",
    "PORTA_ORIGEM": 61,
    "PORTA_DESTINO": 68,
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
                          protocol=SOCK_RAW  # Remover caso for usar apenas ethernet
                          )

    server.run_server()


if __name__ == "__main__":
    main()
