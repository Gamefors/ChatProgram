from utils.MysqlHelper import MysqlHelper#pylint: disable=E0611,E0401

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

	def updateClientRank(self, clientObject, newRank):
		clientObject.rank = newRank		
	
	def ipExists(self, ip):
		ipExists = False
		for clientObject in self.clientList:
			if clientObject.ip == ip:
				ipExists = True
		return ipExists
	
	def usernameExists(self, username):
		usernameExists = False
		for clientObject in self.clientList:
			if clientObject.username.lower() == username.lower():
				usernameExists = True
		return usernameExists

	def hasRank(self, clientObject, rank):
		clientObject.rank = MysqlHelper().getAccountRank(clientObject)
		if(clientObject.rank == rank):
			return True
		return False

	def getAdmins(self):
		admins = list()
		for client in self.clientList:
			if client.rank == "admin":
				admins.append(client)
		return admins