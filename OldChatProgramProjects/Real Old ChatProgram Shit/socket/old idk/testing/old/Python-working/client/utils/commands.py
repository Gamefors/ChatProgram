class commands:
	_user = None

	def __init__(self, u):
		self._user = u

	#helper
	def listCurrentChannelClients(self ,currentChannel):
		currentChannelClients  = self._user.executeServer("listCurrentChannelClients", [currentChannel])
		return currentChannelClients
	#end of helper


	def help(self):
		availableCommands = ["listClients"]
		print("Available commands: " + str(availableCommands))

	def logout(self):
		success = self._user.executeServer("logout", ["xxx"])
		if success:
			self._user.requestsUtil.requestChangeChannel()
			print("Successfully logged out.")

	def listClients(self):
		CurrentChannelClients = self.listCurrentChannelClients(self._user.channel)
		#print(CurrentChannelClients)

