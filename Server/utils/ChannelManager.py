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