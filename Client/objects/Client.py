class ClientObject:
    def __init__(self, username, socketObject, ip, port, channel):
        self.username = username
        self.socketObject = socketObject
        self.ip = ip
        self.port = port
        self.channel = channel