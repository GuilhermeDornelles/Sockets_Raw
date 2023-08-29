from rawSocket import RawSocket
from constants import IPV4_TYPE

if __name__ == "__main__":
    socket = RawSocket(source_mac="a4:1f:72:f5:90:52",     # Substituir pelos endereços MAC desejados
                       dest_mac="a4:1f:72:f5:90:98",
                       net_interface="eth0",  # Substituir pelo nome da interface de rede da máquina
                       # protocol=IPV4_TYPE
                       )
    socket.send_package()
