from rawSocket import RawSocket
from constants import IPV4_TYPE

CONFIG = {
    # "MAC_ORIGEM": "a4:1f:72:f5:90:52",
    "MAC_ORIGEM": "02:42:24:86:f7:fd",
    "MAC_DESTINO": "a4:1f:72:f5:90:98",
    "IP_ORIGEM": "192.168.0.1",
    "IP_DESTINO": "192.168.0.1",
    "INTERFACE_REDE": "eth0"
}


def main():
    socket = RawSocket(source_mac=CONFIG["MAC_ORIGEM"],     # Substituir pelos endereços MAC desejados
                       dest_mac=CONFIG["MAC_DESTINO"],
                       source_ip=CONFIG["IP_ORIGEM"],
                       dest_ip=CONFIG["IP_DESTINO"],
                       # Substituir pelo nome da interface de rede da máquina
                       net_interface=CONFIG["INTERFACE_REDE"],
                       protocol=IPV4_TYPE  # Remover caso for usar apenas ethernet
                       )

    socket.send_package(data="mensagem de teste")


if __name__ == "__main__":
    main()
