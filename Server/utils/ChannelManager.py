class ChannelManager:
	channelList = list()
		
	def addChannel(self, channelObject):
		self.channelList.append(channelObject)

	def removeChannel(self, channelObject):
		self.channelList.remove(channelObject)

	def removeChannelMember(self, channelObject, ClientObject):
		channelObject.clientList.remove(ClientObject)

	def addChannelMember(self, channelObject, ClientObject):
		channelObject.clientList.append(ClientObject)

	def channelExists(self, channel):
		channelExists = False
		for channelObject in self.channelList:
			if channelObject.name == channel:
				channelExists = True
				break
		return channelExists

	def channelContains(self, clientObject, channel):
		channelContains = False
		for channelObject in self.channelList:
			if channelObject.name == channel:
				for client in channelObject.clientList:
					if client == clientObject:
						channelContains = True
						break
		return channelContains