class ClientManager:
	clientList = list()
		
	def addClient(self, clientObject):
		self.clientList.append(clientObject)

	def removeClient(self, clientObject):
		self.clientList.remove(clientObject)

	def updateClientUsername(self, clientObject, newUsername):
		clientObject.username = newUsername

	def updateClientChannelObject(self, clientObject, newChannelObject):
		clientObject.channelObject = newChannelObject
			
	def ipExists(self, ip):
		ipExists = False
		for clientObject in self.clientList:
			if clientObject.ip == ip:
				ipExists = True
				break
		return ipExists
