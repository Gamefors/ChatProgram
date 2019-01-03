class Client:
    def __init__(self, socketObject, username, channelObject, banTime):
        self.socketObject = socketObject
        self.username = username
        self.channelObject = channelObject#should be set to welcome channel on connect
        self.banTime = banTime#default is zero not used atm
        self.ip = self.socketObject.getpeername()[0]
        self.port = self.socketObject.getpeername()[1]