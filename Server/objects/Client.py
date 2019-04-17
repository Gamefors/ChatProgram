class Client:
    def __init__(self, socketObject, username, channelObject, rank):
        self.rank =  rank
        self.username = username
        self.socketObject = socketObject      
        self.channelObject = channelObject
        self.ip = self.socketObject.getpeername()[0]
        self.port = self.socketObject.getpeername()[1]