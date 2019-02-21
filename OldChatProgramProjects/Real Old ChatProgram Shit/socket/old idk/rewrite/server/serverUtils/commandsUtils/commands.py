import json
import time
import socket
import random
import sys

from serverUtils.packetsUtils.packet import packet
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
		self.availableCommands["listUsers"] = CmdListUsers("/listUsers", "listUsers", [], "Shows you a list of all users logged in", self._server)
		self.availableCommands["listChannels"] = CmdListChannels("/listChannels", "listChannels", [], "Shows you a list of all channels", self._server)
		self.availableCommands["listBannedClients"] = CmdListBannedClients("/listBannedClients", "listBannedClients", [], "Shows you a list of all banned clients", self._server)
		self.availableCommands["kick"] = CmdKick("/kick <name>", "kick", ["<name>"], "Kicks the stated username or ip address from server", self._server)
		self.availableCommands["ban"] = CmdBan("/ban <ip>", "ban", ["<ip>"], "Bans the stated ip from the server", self._server)
		self.availableCommands["pardon"] = CmdPardon("/pardon <ip>", "pardon", ["<ip>"], "Pardons the stated ip from the server", self._server)
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
			print(self._server.serverPrefix + "No clients connected")
		for client in self._server.users:
			print(str(client[1][0]) + ":" + str(client[1][1]) + " connected")

class CmdListUsers(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		if len(self._server.loggedInUsers) is 0:
			print(self._server.serverPrefix + "No users logged in")
		for user in self._server.loggedInUsers:
			print(str(user) + " logged in")

class CmdListChannels(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		for channel, desc in self._server.mysqlHelperUtil.getChannels().items():
			print(channel + ": " + desc)

class CmdListBannedClients(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		for ip, banned in self._server.mysqlHelperUtil.getBannedClients().items():
			if "0" not in str(banned):
				print(ip + " is banned")
		if "0" in str(banned):
			print(self._server.serverPrefix + "No one is banned from the server")
		
class CmdKick(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		if len(self._server.loggedInUsers) is 0:
			print(self._server.serverPrefix + "No clients to kick logged in")
		else:
			success = False
			for user in self._server.loggedInUsers:
				for key, value in user.items():
					if value == args[0]:
						for user in self._server.users:
							if user[1][0] == key:
								self._server.sendPacketToClient(packet("5", "kick", ["True"], user))
						success = True
						self._server.createLogsUtil.printandwriteserverlog(self._server.serverPrefix + args[0] + " got kicked from the channel")
			if not success:
				print(self._server.serverPrefix + args[0] + " does not exists or is not online")

class CmdBan(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		if len(self._server.users) is 0:
			print(self._server.serverPrefix + "No clients to ban connected to the server")
		else:
			success = False
			for user in self._server.users:
				if user[1][0] == args[0]:
					self._server.mysqlHelperUtil.ban(args[0])
					success = True
					self._server.sendPacketToClient(packet("4", "ban", ["True"], user))
					user[0].shutdown(socket.SHUT_RDWR)
					user[0].close()
					self._server.createLogsUtil.printandwriteserverlog(self._server.serverPrefix + args[0] + " got banned from server")
			if not success:
				print(self._server.serverPrefix + args[0] + " does not exists or is not online")

class CmdPardon(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		success = self._server.mysqlHelperUtil.pardon(args[0])
		if success:
			self._server.createLogsUtil.printandwriteserverlog(self._server.serverPrefix + args[0] + " got pardoned from server")
		else:
			print(self._server.serverPrefix + args[0] + " ip does not exists or is already unbanned")

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
		print(self._server.serverPrefix + "stopped server")
		for user in self._server.users:
			self._server.sendPacketToClient(packet("8", "shutdown", ["True"], user))
			user[0].shutdown(socket.SHUT_RDWR)
			user[0].close()
		print("please stop the server by closing the script ctrl+c or shuting down the machine where the server runs on")

class CmdHelp(command):
	def __init__(self, syntax, commandName, arguments, description, server_):
		super().__init__(syntax, commandName, arguments, description, server_)
	def execute(self, args):
		for cmdName, cmd in self._server.commandsUtil.availableCommands.items():
			print(cmd.syntax + ": " + cmd.description)