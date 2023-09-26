from socket import SOCK_DGRAM
import threading
from models.serverSocket import ChatServerSocket, ControlServerSocket
from models.chat import Chat

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
    
    chat_socket = ChatServerSocket(data_port=CONFIG["PORTA_DADOS"], source_ip=CONFIG["IP_ORIGEM"])
    control_socket = ControlServerSocket(control_port=CONFIG["PORTA_CONTROLE"], source_ip=CONFIG["IP_ORIGEM"])

    chat_socket.bind_server()
    control_socket.bind_server()

    chat_thread = threading.Thread(target=chat_socket.receive_package, daemon=True)
    control_thread = threading.Thread(target=control_socket.receive_package, daemon=True)

    chat_thread.start()
    control_thread.start()

    #logica do chat

    chat = Chat(chat_socket=chat_socket, control_socket=control_socket)
    chat.start()

    print("iniciou o chat")


if __name__ == "__main__":
    main()
