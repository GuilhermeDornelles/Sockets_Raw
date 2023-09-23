class Command:
    def __init__(self, source_port: int, source_ip: str, data: str):
        self.source_ip = source_ip
        # self.dest_ip = dest_ip
        self.source_port = source_port
        # self.dest_port = dest_port
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
