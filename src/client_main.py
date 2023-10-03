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
    client = ClientSocket(dest_ip=CONFIG["IP_DESTINO"], protocol=SOCK_DGRAM)

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
    except Exception:
        super_print("Erro ao se registrar, finalizando")
        exit(-1)
    if connected:
        super_print("Cliente registrado com sucesso.")
    command = ""
    while connected:
        try:
            print("Tipos de comandos disponíveis para interação no CHAT:")
            print(
                " /privmsg <nome-destino> <mensagem> -> envia mensagem privada para cliente específico")
            print(" /msg <mensagem> -> envia mensagem para todos os clientes conectados")
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
    super_print("Desconectando do servidor...")
    return True


def main():
    run_client_interface()


if __name__ == "__main__":
    main()
