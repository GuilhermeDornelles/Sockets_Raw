class Client:
    def __init__(self, ip: int, port: int, name: str):
        self.port = port
        self.ip = ip
        self.name = name

    def __repr__(self):
        return f"(Client: '{self.name}' - Address: {self.ip}:{self.port})"
