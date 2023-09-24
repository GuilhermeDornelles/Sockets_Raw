from enum import Enum


class CommandsEnum(Enum):
    EXIT = "/exit"
    CONNECT = "/connect"
    PRIVMSG = "/privmsg"
    MSG = "/msg"
