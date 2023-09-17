class Message:
    def __init__(self, source_port, dest_port, source_ip, dest_ip, source_mac, dest_mac, data):
        self.source_mac = source_mac
        self.dest_mac = dest_mac
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.source_port = source_port
        self.dest_port = dest_port
        self.data = data

    def __str__(self) -> str:
        return f"""
    source ip = {self.source_ip};
    dest ip = {self.dest_ip};
    source port = {self.source_port};
    dest port = {self.dest_port};
    data = '{self.data}';
"""
