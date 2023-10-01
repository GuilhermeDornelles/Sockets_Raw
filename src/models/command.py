from models.commands_enum import CommandsEnum


class Command:
    def __init__(self, source_port: int, source_ip: str, data: str):
        self.source_ip = source_ip
        # self.dest_ip = dest_ip
        self.source_port = source_port
        # self.dest_port = dest_port
        self.options = list()
        self.command, self.options = self._split_data(data)

    def __str__(self) -> str:
        return f"""
Command: '{self.command}';
    options = {self.options};
    source ip = {self.source_ip};
    source port = {self.source_port};
"""

    def _split_data(self, data: str):
        parts = data.split(" ")
        return parts[0], parts[1:]

    @staticmethod
    def command_is_valid(command: 'Command') -> bool:
        return command.command in [member.value for member in CommandsEnum]

    @staticmethod
    def validate_command_options(command: 'Command') -> bool:
        if command.command == CommandsEnum.CONNECT.value:
            return len(command.options) == 1
        elif command.command == CommandsEnum.EXIT.value:
            return len(command.options) == 0
        elif command.command == CommandsEnum.PRIVMSG.value:
            return len(command.options) == 2
        elif command.command == CommandsEnum.MSG.value:
            return len(command.options) == 1
        else:
            return False
