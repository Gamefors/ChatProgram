import json
class commands:

	_server = None

	availableCommands = dict()

	def __init__(self, server_):
		self._server = server_

		self.availableCommands["listClients"] = CmdListClients("/listClients", "listClients", [], "Shows you a list of all clients connected to the server", self._server)
		self.availableCommands["listChannels"] = CmdListChannels("/listChannels", "listChannels", [], "Shows you a list of all channels", self._server)
		self.availableCommands["kick"] = CmdKick("/kick <ip>|<name>", "kick", ["ip|name"], "Kicks the stated username or ip address from server", self._server)
		self.availableCommands["ban"] = CmdBan("/ban <ip>|<name>", "ban", ["ip|name"], "Bans the stated username from the server", self._server)
		self.availableCommands["editChannel"] = CmdEditChannel("/editChannel <channelName> <attribute> <newValue>", "editChannel", ["channelName", "attribute", "newValue"], "Edits the stated <attribute> from <channelName> to <newValue>. Attributes: name, description, password, auth_level", self._server)
		self.availableCommands["createChannel"] = CmdCreateChannel("/createChannel <channelName> <description> <[password]> <[auth_level]>", "createChannel", ["channelName", "description", "[password]", "[auth_level]"], "Creates channel with the stated attributes.", self._server)
		self.availableCommands["deleteChannel"] = CmdDeleteChannel("/deleteChannel <channelName>", "deleteChannel", ["channelName"], "Deletes the stated channel", self._server)
		self.availableCommands["setUserAuthLevel"] = CmdSetUserAuthLevel("/setUserAuthLevel <username> <authLevel>", "setUserAuthLevel", ["username", "authLevel"], "Sets the stated users authlevel to the new given authlevel.", self._server)
		self.availableCommands["help"] = CmdHelp("/help", "help", [], "Shows a help page", self._server)


class command:

	commandName = None
	syntax = None
	arguments = None
	description = None
	_server = None

	def __init__(self, syntax_, commandName_, arguments_, description_, server_):
		self.syntax = syntax_
		self.commandName = commandName_
		self.arguments = arguments_
		self.description = description_
		self._server = server_

	def correctArgs(self, args):
		cMin = 0
		for arg in self.arguments:
			if (not arg.startswith("[")) and (not arg.endswith("]")):
				cMin = cMin + 17

		cMax = 0
		for arg in self.arguments:
				cMax = cMax + 1

		return (len(args) >= cMin) and (len(args) <= cMax)






class CmdListClients(command):

	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)

	def execute(self, args):
		if len(self._server.users) is 0:
			self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + "No clients connected")
		for user in self._server.users:
			self._server.createlogUtil.printandwriteserverlog(str(user.address[0]) + ":" + str(user.address[1]) + " as user " + str(user.username) + " in channel " + str(user.channel))

class CmdListChannels(command):

	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)

	def execute(self, args):
		channels = self._server.mysqlHelperUtil.getChannels()
		channel = [(json.dumps(channels))]
		print(channel)

class CmdKick(command):

	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)

	def execute(self, args):
		var = None
		#execute

class CmdBan(command):

	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)

	def execute(self, args):
		var = None
		#execute

class CmdEditChannel(command):

	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)

	def execute(self, args):
		success = self._server.mysqlHelperUtil.editChannel(args[0], args[1], args[2])
		if not success:
			print("the channel " + args[0] + " does not exists")

class CmdCreateChannel(command):

	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)

	def execute(self, args):
		success = self._server.mysqlHelperUtil.createChannel(args[0], args[1], args[2] if len(args) > 2 else None, args[3] if len(args) > 3 else None)
		if not success:
			print("channel " + args[0] + " did not get created")

class CmdDeleteChannel(command):

	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)

	def execute(self, args):
		success = self._server.mysqlHelperUtil.deleteChannel(args[0])
		if not success:
			print("channel " + channelName + " does not exits")

class CmdSetUserAuthLevel(command):

	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)

	def execute(self, args):
		success = self._server.mysqlHelperUtil.changeAuth_level(args[0], args[1])
		if not success:
			print("user '" + username + "' does not exits")


class CmdHelp(command):

	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)

	def execute(self, args):
		for cmdName, cmd in self._server.commandsUtil.availableCommands.items():
			print(cmd.syntax + ": " + cmd.description)