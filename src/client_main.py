from socket import SOCK_DGRAM, SOCK_STREAM
from models.commands_enum import CommandsEnum
from models.clientSocket import ClientSocket, ClientSocketTCP, ClientSocketUDP
from utils import super_print
import os
import signal

CONFIG = {
    "IP_ORIGEM": "127.0.0.1",
    "IP_DESTINO": "127.0.0.1",         # Substituir pelos endereços IP desejados
    "PORTA_ORIGEM": 61,
    "PORTA_DESTINO": 12346,
}

DATA_PORT = 12345
CONTROL_PORT = 12346

SOCKET_PROTOCOL = SOCK_DGRAM    # UDP
# SOCKET_PROTOCOL = SOCK_STREAM     # TCP


def run_client_interface():
    if SOCKET_PROTOCOL == SOCK_STREAM:
        client = ClientSocketTCP(
            dest_ip=CONFIG["IP_DESTINO"], protocol=SOCKET_PROTOCOL, disconnect_function=disconnect, dest_port=DATA_PORT)

    elif SOCKET_PROTOCOL == SOCK_DGRAM:
        client = ClientSocketUDP(
            dest_ip=CONFIG["IP_DESTINO"], protocol=SOCKET_PROTOCOL, disconnect_function=disconnect)

    try:
        connected = False
        client.start()
        super_print("BEM VINDO AO CHAT")
        client_name = str(
            input("Insira seu nome para se registrar no servidor: "))
        print(f"Nome do cliente: {client_name}")
        try:
            client.send_package(
                f"{CommandsEnum.CONNECT.value} {client_name}", dest_port=CONTROL_PORT)
            connected = True
        except Exception as e:
            print(e)
            disconnect(-1)
        if connected:
            super_print("Cliente registrado com sucesso.")
        command = ""
        while connected:
            print("Comandos disponíveis para interação no CHAT:")
            print(
                " /privmsg <nome-destino> <mensagem> -> envia mensagem privada para cliente específico")
            print(" /msg <mensagem> -> envia mensagem para todos os clientes conectados")
            print(
                " /privfile <nome-destino> <filepath> -> envia um arquivo para o cliente específico")
            print(
                " /file <filepath> -> envia um arquivo para todos os clientes conectados")
            print(" /exit -> desconecta do CHAT")
            print("Envie um comando:")
            command = str(input()).strip()

            tp = command.split()[0]
            if tp in [member.value for member in CommandsEnum]:
                if command == CommandsEnum.EXIT.value:
                    client.send_package(command, dest_port=CONTROL_PORT)
                    connected = False
                else:
                    client.send_package(command, dest_port=DATA_PORT)
                print("\nComando enviado ao servidor.\n")
            else:
                print("\nComando desconhecido.\n")
    except KeyboardInterrupt:
        client.send_package("/exit", dest_port=CONTROL_PORT)
        connected = False
        disconnect()
    return True


def disconnect(exit_code: int = 0):
    if exit_code == -1:
        super_print("Erro ao se registrar, finalizando sessão")
    elif exit_code == -2:
        super_print("Servidor desconectado, finalizando sessão")
    elif exit_code == -3:
        super_print("Nome ou porta já utilizado")
    else:
        super_print("Desconectando do servidor...")
    os.kill(os.getpid(), signal.SIGTERM)


def main():
    run_client_interface()


if __name__ == "__main__":
    main()
