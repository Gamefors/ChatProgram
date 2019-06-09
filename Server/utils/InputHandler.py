from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611, E0401
from utils.ChannelManager import ChannelManager#pylint: disable=E0611, E0401
from utils.ClientManager import ClientManager#pylint: disable=E0611, E0401
from utils.FileHelper import FileHelper#pylint: disable=E0611, E0401
from utils.LogHelper import LogHelper#pylint: disable=E0611, E0401

from utils.MysqlHelper import MysqlHelper#pylint: disable=E0611, E0401

from objects.Channel import Channel#pylint: disable=E0611, E0401
from objects.Command import Command#pylint: disable=E0611, E0401

import os, datetime, time, sys

class InputHandler:
	
	commandList = list()
			
	def importScripts(self):
		self.decEncHelper = DecodingEncodingHelper()
		self.channelManager = ChannelManager()
		self.clientManager = ClientManager()
		self.fileHelper = FileHelper()
		self.logHelper = LogHelper()

		self.mysqlHelper = MysqlHelper()

	def createCommand(self, name, syntax, arguments, description):
		command = Command(name, syntax, arguments, description)
		self.commandList.append(command)
		return command

	def initializeCommands(self):
		self.cmdListClients = self.createCommand("listClients", "/listClients", "NONE", "Lists all connected clients with their name, ip and channel their in.")
		self.cmdClear = self.createCommand("Clear", "/clear", "NONE", "Clears your interpreter console.")	
		self.cmdHelp = self.createCommand("Help", "/help", "NONE", "Shows a list of available commands.")
		self.cmdKick = self.createCommand("Kick", "/kick <name/ip>", "<NAME/IP>", "Kicks the given IP from the server.")
		self.cmdBan = self.createCommand("Ban", "/ban <name/ip> <time>", "<NAME/IP> <TIME>", "Bans the specified client for the given amount of time in minutes.")
		self.cmdMonitorMode = self.createCommand("monitorMode", "/monitorMode", "NONE", "Switches to monitor mode.")
		self.cmdChangeRank = self.createCommand("changeRank", "/changeRank <name/ip> <rank>", "<NAME/IP> <RANK>", "Changes the rank of the given client.")
		self.cmdListChannel = self.createCommand("listChannel", "/listChannel", "NONE", "Lists all channels with their belonging clients.")
		self.cmdCreateChannel = self.createCommand("createChannel", "/createChannel <name> <description> <password> <accessLevel>", "<NAME/DESCRIPTION/PASSWORD/ACCESSLEVEL>", "Creates a temporary Channel.")
		self.cmdRemoveChannel = self.createCommand("removeChannel", "/removeChannel <name>", "<NAME>", "Removes the give Channel.")
		
	def __init__(self, upTime):
		self.upTime = upTime
		#Imports
		self.importScripts()
		#Create Commands
		self.initializeCommands()
	
	def handleInput(self, command):
		command = command.split()

		if command[0] == self.cmdClear.name:
			os.system('cls' if os.name=='nt' else 'clear')

		elif command[0] == self.cmdListClients.name:
			if len(self.clientManager.clientList) < 1:
				self.logHelper.log("error", "No clients connected")
			else:
				self.logHelper.log("error", "Connected clients:")
				for clientObject in self.clientManager.clientList:
					self.logHelper.log("info", clientObject.ip + " with name " + clientObject.username + " in " + clientObject.channelObject.name)
		
		elif command[0] == self.cmdHelp.name:
			self.logHelper.log("info", "Commands:")
			self.logHelper.log("info", "----------------------------------------------------------")
			for command in self.commandList:
				self.logHelper.log("info", command.syntax + " : " + command.description)
			self.logHelper.log("info", "----------------------------------------------------------")
		
		elif command[0] == self.cmdKick.name:
			if len(self.clientManager.clientList) < 1:
				self.logHelper.log("error", "No clients connected")
			else:
				client = None
				try:
					client = command[1]
				except IndexError:
					self.logHelper.log("error", "Syntax: " + self.cmdKick.syntax)
				if client != None:
					if self.clientManager.ipExists(client):
						for clientObject in self.clientManager.clientList:
							if clientObject.ip == client:
								self.logHelper.log("info", clientObject.ip + " : " + clientObject.username + " got kicked")						
								clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("402"))
								clientObject.socketObject.close()
					elif self.clientManager.usernameExists(client):
						for clientObject in self.clientManager.clientList:
							if clientObject.username.lower() == client:
								self.logHelper.log("info", clientObject.ip + " : " + clientObject.username + " got kicked")						
								clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("402"))
								clientObject.socketObject.close()
					else:
						self.logHelper.log("error", "Your given Ip/Name doesn't exist.")
						
		elif command[0] == self.cmdBan.name:
			if len(self.clientManager.clientList) < 1:
				self.logHelper.log("error", "No clients connected")
			else:
				client = None
				banTime = None
				try:
					client = command[1]
					banTime = int(command[2])
				except IndexError:
					if client or banTime == None:
						self.logHelper.log("error", "Syntax: " + self.cmdBan.syntax)
				if client != None:
					if self.clientManager.ipExists(client):
						for clientObject in self.clientManager.clientList:
							if clientObject.ip == client:
								if banTime != None:
									if banTime == 0:
										self.fileHelper.addClientToBanList(clientObject.ip)
										self.logHelper.log("info", clientObject.ip + " : " + clientObject.username + " got permanantly banned")						
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "You got permanantly banned by the console"))
										clientObject.socketObject.close()
									else:
										currentTimeStamp = datetime.datetime.now().timestamp()
										self.fileHelper.addClientToBanList(clientObject.ip + ":" + str(currentTimeStamp + int(banTime)*60))
										self.logHelper.log("info", clientObject.ip + " : " + clientObject.username + " got banned for " + str(banTime) + "minutes")						
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "You got banned for " + str(banTime) + " minutes by the console"))
										clientObject.socketObject.close()
								else:
									self.fileHelper.addClientToBanList(clientObject.ip)
									self.logHelper.log("info", clientObject.ip + " : " + clientObject.username + " got permanantly banned")						
									clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "You got permanantly banned by the console"))
									clientObject.socketObject.close()
					elif self.clientManager.usernameExists(client):
						for clientObject in self.clientManager.clientList:
							if clientObject.username.lower() == client:
								if banTime != None:
									if banTime == 0:
										self.fileHelper.addClientToBanList(clientObject.ip)
										self.logHelper.log("info", clientObject.ip + " : " + clientObject.username + " got permanantly banned")						
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "You got permanantly banned by the console"))
										clientObject.socketObject.close()
									else:
										currentTimeStamp = datetime.datetime.now().timestamp()
										self.fileHelper.addClientToBanList(clientObject.ip + ":" + str(currentTimeStamp + int(banTime)*60))
										self.logHelper.log("info", clientObject.ip + " : " + clientObject.username + " got banned for " + str(banTime) + "minutes")						
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "You got banned for " + str(banTime) + " minutes by the console"))
										clientObject.socketObject.close()
								else:
									self.fileHelper.addClientToBanList(clientObject.ip)
									self.logHelper.log("info", clientObject.ip + " : " + clientObject.username + " got permanantly banned")						
									clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "You got permanantly banned by the console"))
									clientObject.socketObject.close()
					else:
						print("[Server/Error] Your given Ip/Name doesn't exist.")
						
		elif command[0] == self.cmdListChannel.name:
			self.logHelper.log("info", "Channels:")
			self.logHelper.log("info", "----------------------------------------------------------")
			for channel in self.channelManager.channelList:
				self.logHelper.log("info", "-" + channel.name + " : Description:" + channel.description)
				self.logHelper.log("info", " Clients:")
				if len(channel.clientList) < 1:
					self.logHelper.log("info", " -channel is empty")
				else:
					for client in channel.clientList:
						self.logHelper.log("info", " -" + client.ip + " : " + client.username)
			self.logHelper.log("info", "----------------------------------------------------------")

		elif command[0] == self.cmdCreateChannel.name:#TODO: add things to remove user error when acces level isnst int and description contains spaces 
			name = None
			description = None
			password = None
			accessLevel = None
			try:
				name = command[1]
				description = command[2]
				password = command[3]
				accessLevel = int(command[4])
				self.channelManager.addChannel(Channel(name, description, password, accessLevel, list()))
				self.logHelper.log("info", "Channel " + name + " created.")
			except:
				if name or description or password or accessLevel == None:
					self.logHelper.log("error", "Syntax: " + self.cmdCreateChannel.syntax)
			
		elif command[0] == self.cmdRemoveChannel.name:
			name = None
			try:
				name = command[1]
				for channel in self.channelManager.channelList:
					if channel.name == name:
						self.channelManager.removeChannel(channel)
				self.logHelper.log("info", "Channel " + name + " was removed.")
			except:
				if name == None:
					self.logHelper.log("error", "Syntax: " + self.cmdRemoveChannel.syntax)

		elif command[0] == self.cmdChangeRank.name:#TODO: add things to remove user error for rank and check if rank isnt even a rank
			if len(self.clientManager.clientList) < 1:
				self.logHelper.log("error", "No clients connected")
			else:
				client = None
				rank = None
				try:
					client = command[1]
					rank = command[2]
				except IndexError:
					self.logHelper.log("error", "Syntax: " + self.cmdChangeRank.syntax)
				if client != None:
					if rank != None:
						if self.clientManager.ipExists(client):
							for clientObject in self.clientManager.clientList:
								if clientObject.ip == client:
									prevRank = clientObject.rank
									clientObject.rank = rank
									self.mysqlHelper.updateAccountRank(clientObject)
									self.logHelper.log("info", "Changed " + clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " 's rank from " + prevRank + " to " + rank)						
								
						elif self.clientManager.usernameExists(client):
							for clientObject in self.clientManager.clientList:
								if clientObject.username.lower() == client:
									prevRank = clientObject.rank
									clientObject.rank = rank
									self.mysqlHelper.updateAccountRank(clientObject)
									self.logHelper.log("info", "Changed " + clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " 's rank from " + prevRank + " to " + rank)						
						else:
							self.logHelper.log("error", "Your given Ip/Name doesn't exist.")
	
		elif command[0] == self.cmdMonitorMode.name:
			monitor = True
			config = self.fileHelper.getConfig("Server Config")
			ip = config.ip + ":" + str(config.port)
			if len(ip) != 20:
				ip = " "*(20 - len(ip)) + ip
			while monitor:
				clearCount = 0
				connectedClients = str(len(self.clientManager.clientList))
				connectedAdmins = str(len(self.clientManager.getAdmins()))
				if len(connectedClients) != 3:
					connectedClients = "0"*(3 - len(connectedClients)) + connectedClients
				if len(connectedAdmins) != 3:
					connectedAdmins = "0"*(3 - len(connectedAdmins)) + connectedAdmins
				os.system('cls' if os.name=='nt' else 'clear')
				try:																
					print("##############Monitoring##############\n#Server Ip/Port: " + ip + "#\n#Uptime:                     " + time.strftime('%H:%M:%S', time.gmtime(int(time.time() - self.upTime))) + "#\n#Connected Clients:               " + connectedClients + "#\n#Connected Admins:                " + connectedAdmins + "#\n##############Monitoring##############")
					while clearCount != 5:	
						sys.stdout.write("\x1b[1A")
						sys.stdout.write("\x1b[2K")
						clearCount = clearCount + 1
					time.sleep(0.5)
				except KeyboardInterrupt:
					monitor = False
					os.system('cls' if os.name=='nt' else 'clear')
					self.logHelper.log("info", "Exited monitor mode.")	
		
		else:
			self.logHelper.log("error", "Unknown command: " + command[0])
			self.logHelper.log("error", "type /help for a list of commands")