from socket import SOCK_DGRAM
from models.commands_enum import CommandsEnum
from models.clientSocket import ClientSocket
from utils import super_print

CONFIG = {
    "IP_ORIGEM": "127.0.0.1",
    "IP_DESTINO": "127.0.0.1",         # Substituir pelos endereços IP desejados
    "PORTA_ORIGEM": 61,
    "PORTA_DESTINO": 12346,
}

DATA_PORT = 12345
CONTROL_PORT = 12346


def run_client_interface():
    socket = ClientSocket(dest_ip=CONFIG["IP_DESTINO"],
                          #   dest_port=CONFIG["PORTA_DESTINO"],
                          protocol=SOCK_DGRAM
                          )

    super_print("BEM VINDO AO CHAT")
    client_name = str(
        input("Insira seu nome para se registrar no servidor: ")).strip()
    print(f"Nome do cliente: {client_name}")
    res = socket.send_package(
        f"{CommandsEnum.CONNECT.value} {client_name}", dest_port=CONTROL_PORT)
    super_print("Cliente registrado com sucesso.")
    command = ""
    while command != CommandsEnum.EXIT.value:
        print("Tipos de comandos disponíveis para interação no CHAT:")
        print(" /privmsg <nome-destino> <mensagem> -> envia mensagem privada para cliente específico")
        print(" /msg <mensagem> -> envia mensagem para todos os clientes conectados")
        print(" /exit -> desconecta do CHAT")
        print("Envie um comando:")
        command = str(input()).strip()
        message = command.split()[1] # Pega a mensagem após o comando
        if CommandsEnum.EXIT.value in command:
            res = socket.send_package(command, dest_port=CONTROL_PORT)
        elif CommandsEnum.PRIVMSG.value in command:
            res = socket.send_package(command, dest_port=DATA_PORT)
        elif CommandsEnum.MSG.value in command:
            res = socket.send_package(f"{CommandsEnum.MSG.value} {message}", dest_port=DATA_PORT)
        else :
            print("Comando enviado ao servidor.")
    super_print("Desconectando do servidor...")
    return


def main():
    run_client_interface()
    # socket = ClientSocket(dest_ip=CONFIG["IP_DESTINO"],
    #                       #   dest_port=CONFIG["PORTA_DESTINO"],
    #                       protocol=SOCK_DGRAM
    #                       )

    # socket.send_package(data="/CONNECT", dest_port=12345)
    # socket.send_package(data="Qualquer coisa", dest_port=12346)
    # socket.send_package(data="Teste dois !")


if __name__ == "__main__":
    main()
