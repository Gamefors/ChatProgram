class Channel:
    def __init__(self, name, description, password, accessLevel, clientList):
        self.name = name
        self.description = description
        self.password = password
        self.accessLevel = accessLevel
        self.clientList = clientList