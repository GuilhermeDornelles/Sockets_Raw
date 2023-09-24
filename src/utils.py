import socket
from struct import pack
import re


def get_checksum(data):
    checksum = 0

    data_len = len(data)
    if (data_len % 2):
        data_len += 1
        data += pack('!B', 0)

    # Divida o cabeçalho em palavras de 16 bits e some-as
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + data[i + 1]
        checksum += w
    # Some o excesso de carry de 16 bits para obter o resultado final
    while (checksum >> 16) > 0:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    # Faça o complemento de 1 do resultado
    checksum = ~checksum & 0xFFFF
    print(checksum)
    return checksum


def format_and_validate_ip(ip: str):
    aux_ip = ip.replace(".", "")
    try:
        int(aux_ip)
        if not re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", "127.0.0.1"):
            raise Exception

        result = socket.inet_aton(ip)
    except Exception as e:
        raise e
    return result


def format_and_validate_mac(mac: str):
    aux_mac = mac.replace(":", "")
    try:
        if len(aux_mac) != 12:
            raise Exception
        if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
            raise Exception

        result = bytes.fromhex(aux_mac)
    except Exception as e:
        raise e
    return result


def super_print(text: str):
    length = len(text)
    print("#" * (length+6))
    print(f"## {text} ##")
    print("#" * (length+6))
