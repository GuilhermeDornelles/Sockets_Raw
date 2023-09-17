from models.serverSocket import ServerSocket
from socket import IPPROTO_UDP

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
    server = ServerSocket(source_mac=CONFIG["MAC_ORIGEM"],
                          dest_mac=CONFIG["MAC_DESTINO"],
                          source_ip=CONFIG["IP_ORIGEM"],
                          data_port=CONFIG["PORTA_DADOS"],
                          control_port=CONFIG["PORTA_CONTROLE"],
                          protocol=IPPROTO_UDP
                          #   dest_ip=CONFIG["IP_DESTINO"],
                          #   dest_port=CONFIG["PORTA_DESTINO"],
                          #   net_interface=CONFIG["INTERFACE_REDE"],
                          )

    server.run_server()


if __name__ == "__main__":
    main()
