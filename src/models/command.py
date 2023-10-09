from models.commands_enum import CommandsEnum


class Command:
    def __init__(self, source_port: int, source_ip: str, data: str):
        self.source_ip = source_ip
        self.source_port = source_port
        self.type = None
        self.dest_name = None
        self.data = None
        self.file_path = None
        self._split_data(data)

    def __repr__(self) -> str:
        return f"""
            Command_type: '{self.type}';
            Destination_name: {self.dest_name};
            Data: {self.data};
            Source_address: {self.source_ip}:{self.source_port}.
        """

    # Atribui os campos conforme o tipo da mensagem
    def _split_data(self, data: str):
        parts = data.split(" ")
        self.type = parts[0]
        dt = ''
        if self.type == CommandsEnum.PRIVMSG.value:
            self.dest_name = parts[1]
            for pt in parts[2:]:
                dt += " " + pt
        elif self.type in [CommandsEnum.CONNECT.value, CommandsEnum.MSG.value]:
            for pt in parts[1:]:
                dt += " " + pt
        elif self.type == CommandsEnum.FILE.value:
            self.file_path = parts[1]
            dt = data.split(self.file_path)[-1]
        elif self.type == CommandsEnum.PRIVFILE.value:
            self.dest_name = parts[1]
            self.file_path = parts[2]
            dt = data.split(self.file_path)[-1]

        if (dt):
            self.data = dt.strip()

    @staticmethod
    def type_is_valid(command: 'Command') -> bool:
        return command.type in [member.value for member in CommandsEnum]
