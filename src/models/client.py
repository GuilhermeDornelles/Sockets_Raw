class Client:
    def __init__(self, ip: int, port: int, name: str):
        self.port = port
        self.ip = ip
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
