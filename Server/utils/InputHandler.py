from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611, E0401
from utils.ChannelManager import ChannelManager#pylint: disable=E0611, E0401
from utils.ClientManager import ClientManager#pylint: disable=E0611, E0401
from utils.FileHelper import FileHelper#pylint: disable=E0611, E0401
from utils.LogHelper import LogHelper#pylint: disable=E0611, E0401

from objects.Channel import Channel#pylint: disable=E0611, E0401
from objects.Command import Command#pylint: disable=E0611, E0401

import os, datetime

class InputHandler:
	
	commandList = list()
			
	def importScripts(self):
		self.decEncHelper = DecodingEncodingHelper()
		self.channelManager = ChannelManager()
		self.clientManager = ClientManager()
		self.fileHelper = FileHelper()
		self.logHelper = LogHelper()

	def createCommand(self, name, syntax, arguments, description):
		command = Command(name, syntax, arguments, description)
		self.commandList.append(command)
		return command

	def initializeCommands(self):
		self.cmdListClients = self.createCommand("listClients", "/listClients", "NONE", "Lists all connected clients with their name, ip and channel their in.")
		self.cmdClear = self.createCommand("Clear", "/clear", "NONE", "Clears your interpreter console.")	
		self.cmdHelp = self.createCommand("Help", "/help", "NONE", "Shows a list of available commands.")
		self.cmdKick = self.createCommand("Kick", "/kick <IP>", "IP", "Kicks the given IP from the server.")
		self.cmdBan = self.createCommand("Ban", "/ban <IP> <TIME>", "IP:TIME", "Bans the specified client for the given amount of time in minutes.")
		self.cmdListChannel = self.createCommand("listChannel", "/listChannel", "NONE", "Lists all channels with their belonging clients.")

	def __init__(self):
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
				self.logHelper.printAndWriteServerLog("[Server/Error] No clients connected")
			else:
				self.logHelper.printAndWriteServerLog("[Server/Info] Connected clients:")
				for clientObject in self.clientManager.clientList:
					self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " with name " + clientObject.username + " in " + clientObject.channelObject.name)
		
		elif command[0] == self.cmdHelp.name:
			self.logHelper.printAndWriteServerLog("[Server/Info] Commands:")
			self.logHelper.printAndWriteServerLog("----------------------------------------------------------")
			for command in self.commandList:
				self.logHelper.printAndWriteServerLog(command.syntax + " : " + command.description)
			self.logHelper.printAndWriteServerLog("----------------------------------------------------------")
		
		elif command[0] == self.cmdKick.name:
			if len(self.clientManager.clientList) < 1:
				self.logHelper.printAndWriteServerLog("[Server/Error] No clients connected")
			else:
				client = None
				try:
					client = command[1]
				except IndexError:
					self.logHelper.printAndWriteServerLog("[Server/Error] Syntax: " + self.cmdKick.syntax)
				if client != None:
					if self.clientManager.ipExists(client):
						for clientObject in self.clientManager.clientList:
							if clientObject.ip == client:
								self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " got kicked")						
								clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("402[Client/Info] You got kicked by the console"))
								clientObject.socketObject.close()
					elif self.clientManager.usernameExists(client):
						for clientObject in self.clientManager.clientList:
							if clientObject.username.lower() == client:
								self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " got kicked")						
								clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("402[Client/Info] You got kicked by the console"))
								clientObject.socketObject.close()
					else:
						print("[Server/Error] Your given Ip/Name doesn't exist.")
						
		elif command[0] == self.cmdBan.name:
			if len(self.clientManager.clientList) < 1:
				self.logHelper.printAndWriteServerLog("[Server/Error] No clients connected")
			else:
				client = None
				time = None
				try:
					client = command[1]
					time = int(command[2])
				except IndexError:
					if client == None:
						self.logHelper.printAndWriteServerLog("[Server/Error] Syntax: " + self.cmdBan.syntax)
				if client != None:
					if self.clientManager.ipExists(client):
						for clientObject in self.clientManager.clientList:
							if clientObject.ip == client:
								if time != None:
									if time == 0:
										self.fileHelper.addClientToBanList(clientObject.ip)
										self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " got permanantly banned")						
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "[Client/Info] You got permanantly banned by the console"))
										clientObject.socketObject.close()
									else:
										currentTimeStamp = datetime.datetime.now().timestamp()
										self.fileHelper.addClientToBanList(clientObject.ip + ":" + str(currentTimeStamp + int(time)*60))
										self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " got banned for " + str(time) + "minutes")						
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "[Client/Info] You got banned for " + str(time) + "Minutes by the console"))
										clientObject.socketObject.close()
								else:
									self.fileHelper.addClientToBanList(clientObject.ip)
									self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " got permanantly banned")						
									clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "[Client/Info] You got permanantly banned by the console"))
									clientObject.socketObject.close()
					elif self.clientManager.usernameExists(client):
						for clientObject in self.clientManager.clientList:
							if clientObject.username.lower() == client:
								if time != None:
									if time == 0:
										self.fileHelper.addClientToBanList(clientObject.ip)
										self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " got permanantly banned")						
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "[Client/Info] You got permanantly banned by the console"))
										clientObject.socketObject.close()
									else:
										currentTimeStamp = datetime.datetime.now().timestamp()
										self.fileHelper.addClientToBanList(clientObject.ip + ":" + str(currentTimeStamp + int(time)*60))
										self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " got banned for " + str(time) + "minutes")						
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "[Client/Info] You got banned for " + str(time) + "Minutes by the console"))
										clientObject.socketObject.close()
								else:
									self.fileHelper.addClientToBanList(clientObject.ip)
									self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " got permanantly banned")						
									clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405" + "[Client/Info] You got permanantly banned by the console"))
									clientObject.socketObject.close()
					else:
						print("[Server/Error] Your given Ip/Name doesn't exist.")
						
		elif command[0] == self.cmdListChannel.name:
			self.logHelper.printAndWriteServerLog("[Server/Info] Channels:")
			self.logHelper.printAndWriteServerLog("----------------------------------------------------------")
			for channel in self.channelManager.channelList:
				self.logHelper.printAndWriteServerLog("-" + channel.name + " : Description:" + channel.description)
				self.logHelper.printAndWriteServerLog("  Clients:")
				if len(channel.clientList) < 1:
					self.logHelper.printAndWriteServerLog("  -channel is empty")
				else:
					for client in channel.clientList:
						self.logHelper.printAndWriteServerLog("  -" + client.ip + " : " + client.username)
			self.logHelper.printAndWriteServerLog("----------------------------------------------------------")

		else:
			self.logHelper.printAndWriteServerLog("[Server/Error] Unknown command: " + command[0])
			self.logHelper.printAndWriteServerLog("[Server/Error] type /help for a list of commands")