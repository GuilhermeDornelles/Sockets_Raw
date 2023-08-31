import socket

IPV4_TYPE = 0x0800
UNKNOWN_TYPE = socket.IPPROTO_IP  # FOR TESTS
RAW_TYPE = socket.SOCK_RAW



def get_checksum(data):
    sum = 0
    for index in range(0,len(data), 2):
        word = (ord(data[index]) << 8) + (ord(data[index+1]))
        sum += word
    sum = (sum >> 16) + (sum & 0xffff);
    sum = ~sum & 0xffff
    return sum