class Client:
    def __init__(self, socketObject, username, channelObject, banTime):
        self.socketObject = socketObject
        self.username = username
        self.channelObject = channelObject
        self.banTime = banTime
        self.ip = self.socketObject.getpeername()[0]
        self.port = self.socketObject.getpeername()[1]