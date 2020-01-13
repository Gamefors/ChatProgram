import json
import time
import socket
import random
import sys
class commands:

	#global declarations for class commands
	_server = None
	availableCommands = dict()
	#end of global declarations for class commands

	#constructor for class commands
	def __init__(self, server_):
		self._server = server_
	#end of constructor for class commands

		self.availableCommands["listClients"] = CmdListClients("/listClients", "listClients", [], "Shows you a list of all clients connected to the server", self._server)
		self.availableCommands["listChannels"] = CmdListChannels("/listChannels", "listChannels", [], "Shows you a list of all channels", self._server)
		self.availableCommands["listBannedUsers"] = CmdListBannedUsers("/listBannedUsers", "listBannedUsers", [], "Shows you a list of all banned clients", self._server)
		self.availableCommands["kick"] = CmdKick("/kick <name>", "kick", ["<name>"], "Kicks the stated username or ip address from server", self._server)
		self.availableCommands["ban"] = CmdBan("/ban <name>", "ban", ["<name>"], "Bans the stated username from the server", self._server)
		self.availableCommands["pardon"] = CmdPardon("/pardon <name>", "pardon", ["<name>"], "Pardons the stated username from the server", self._server)
		self.availableCommands["editChannel"] = CmdEditChannel("/editChannel <channelName> <attribute> <newValue>", "editChannel", ["channelName", "attribute", "newValue"], "Edits the stated <attribute> from <channelName> to <newValue>. Attributes: name, description, password, auth_level", self._server)
		self.availableCommands["createChannel"] = CmdCreateChannel("/createChannel <channelName> <description> <[password]> <[auth_level]>", "createChannel", ["channelName", "description", "[password]", "[auth_level]"], "Creates channel with the stated attributes.", self._server)
		self.availableCommands["deleteChannel"] = CmdDeleteChannel("/deleteChannel <channelName>", "deleteChannel", ["channelName"], "Deletes the stated channel", self._server)
		self.availableCommands["setUserAuthLevel"] = CmdSetUserAuthLevel("/setUserAuthLevel <username> <authLevel>", "setUserAuthLevel", ["username", "authLevel"], "Sets the stated users authlevel to the new given authlevel.", self._server)
		self.availableCommands["stop"] = CmdStop("/stop", "stop", [], "Stops the server", self._server)
		self.availableCommands["help"] = CmdHelp("/help", "help", [], "Shows a help page", self._server)


class command:

	#global declarations for class command
	commandName = None
	syntax = None
	arguments = None
	description = None
	_server = None
	#end of global declarations for class command

	#constructor for class command
	def __init__(self, syntax_, commandName_, arguments_, description_, server_):
		self.syntax = syntax_
		self.commandName = commandName_
		self.arguments = arguments_
		self.description = description_
		self._server = server_
	#enf of constructor for class command

	#helper for class command
	def correctArgs(self, args):
		cMin = 0
		for arg in self.arguments:
			if (not arg.startswith("[")) and (not arg.endswith("]")):
				cMin = cMin + 1

		cMax = 0
		for arg in self.arguments:
				cMax = cMax + 1
		return (len(args) >= cMin) and (len(args) <= cMax)
	#end of helper for class command


class CmdListClients(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		if len(self._server.users) is 0:
			print(self._server.serverprefix + "No clients connected")
		for user in self._server.users:
			print(str(user.address[0]) + ":" + str(user.address[1]) + " as user " + str(user.username) + " in channel " + str(user.channel))

class CmdListChannels(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		for channel, desc in self._server.mysqlHelperUtil.getChannels().items():
			print(channel + ": " + desc)

class CmdListBannedUsers(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		for username, banned in self._server.mysqlHelperUtil.getBannedUsers().items():
			if "0" not in str(banned):
				print(username + " is banned")
		if "0" in str(banned):
			print(self._server.serverprefix + "No one is banned from the server")
		





class CmdKick(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		if len(self._server.users) is 0:
			print(self._server.serverprefix + "No clients to kick logged in")
		else:
			success = False
			for user in self._server.users:
				if user.username == args[0]:
					user.sendToClient("you got kicked from the channel")
					user._server.requestsUtil.changeChannel([None], user, -random.randint(1,100000))
					success = True
					self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + args[0] + " got kicked from a channel")
			if not success:
				print(self._server.serverprefix + args[0] + " does not exists or is not online")






class CmdBan(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		if len(self._server.users) is 0:
			print(self._server.serverprefix + "No clients to ban logged in")
		else:
			success = False
			for user in self._server.users:
				if user.username == args[0]:
					user.sendToClient("you got banned from the server")
					user.sendPacket("ban", ["---"])
					self._server.mysqlHelperUtil.ban(args[0])
					success = True
					user.connection.shutdown(socket.SHUT_RDWR)
					user.connection.close()
					self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + args[0] + " got banned from server")
			if not success:
				print(self._server.serverprefix + args[0] + " does not exists or is not online")

class CmdPardon(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		success = self._server.mysqlHelperUtil.pardon(args[0])
		if success:
			self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + args[0] + " got pardoned from server")
		else:
			print(self._server.serverprefix + args[0] + " username does not exists or is already unbanned")

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

class CmdStop(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		print(self._server.serverprefix + "Started stopping server")
		if len(self._server.users) is 0:
			print(self._server.serverprefix + "No clients to disconnect")
		for user in self._server.users:
			user.connection.shutdown(socket.SHUT_RDWR)
			user.connection.close()
			print(self._server.serverprefix + "Disconnected: " + str(user.address[0]))
		print(self._server.serverprefix + "Server stopped gracefully")
		print("please stop the server by closing the script ctrl+c or shuting down the machine where the server runs on")

class CmdHelp(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		for cmdName, cmd in self._server.commandsUtil.availableCommands.items():
			print(cmd.syntax + ": " + cmd.description)