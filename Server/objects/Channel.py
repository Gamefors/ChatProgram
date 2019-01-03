class Channel:
    def __init__(self, name, description, password, accessLevel, clientList):
        self.name = name
        self.description = description
        self.password = password#default should be None
        self.accessLevel = accessLevel#default should be 0
        self.clientList = clientList#should be a list containing all clientObjects that should be in the channel