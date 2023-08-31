from rawSocket import RawSocket
from constants import IPV4_TYPE

CONFIG = {
    "MAC_ORIGEM": "a4:1f:72:f5:90:52",
    "MAC_DESTINO": "a4:1f:72:f5:90:98",
    "IP_ORIGEM": "",
    "IP_DESTINO": "",
    "INTERFACE_REDE": "eth0"
    # "INTERFACE_REDE": "Ethernet 2"
}


def main():
    socket = RawSocket(source_mac=CONFIG["MAC_ORIGEM"],     # Substituir pelos endereços MAC desejados
                       dest_mac=CONFIG["MAC_DESTINO"],
                       net_interface=CONFIG["INTERFACE_REDE"],  # Substituir pelo nome da interface de rede da máquina
                       # protocol=IPV4_TYPE
                       )
    
    print(socket.eth_header)
    # socket.send_package(data="mensagem de teste")


if __name__ == "__main__":
    main()
    
