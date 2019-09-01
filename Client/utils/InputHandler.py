from utils.DecodingEncodingHelper import DecodingEncodingHelper, E0401
from utils.GUIHelper import GUIHelper, E0401

from objects.Command import Command, E0401

import os,time

class InputHandler:
	
	commandList = list()
	
	def initializeCommands(self):
		self.cmdClear = self.createCommand("Clear", "/clear", "NONE", "Clears your interpreter console.")
		self.cmdHelp = self.createCommand("Help", "/help", "NONE", "Shows a list of available commands.")
		self.cmdSetName = self.createCommand("SetName", "/setName <Name>", "NAME", "Changes your name to the specified one.")
		self.cmdListChannel = self.createCommand("ListChannel", "/listChannel", "NONE", "Lists all Channel.")
		self.cmdChangeChannel = self.createCommand("ChangeChannel", "/changeChannel <CHANNEL NAME>", "ChannelName", "Enter the specified channel.")
		self.cmdDisconnect = self.createCommand("Disconnect", "/disconnect", "NONE", "Disconnects you from the server.")
		self.cmdListClients = self.createCommand("ListClients", "/listClients <CHANNEL NAME>", "Channel Name", "Shows you a list of clients connected to the specified channel.")
		self.cmdKick = self.createCommand("Kick", "/kick <name/ip>", "<NAME/IP>", "Kicks the specified client from the server.")
		self.cmdBan = self.createCommand("Ban", "/ban <name/ip> <time>", "<NAME/IP> <TIME>", "Bans the specified client for the given amount of time in minutes.")


	def createCommand(self, name, syntax, arguments, description):
		command = Command(name, syntax, arguments, description)
		self.commandList.append(command)
		return command

	def __init__(self, output):
		#Imports
		self.decEncHelper = DecodingEncodingHelper()
		self.guiHelper = GUIHelper(output)
		#Create Commands
		self.initializeCommands()
	
	def handleInput(self, command, clientObject):
		isCommand = True
		command = command.split()
		try:
			var = command[0]
		except IndexError:
			isCommand = False
			self.guiHelper.printOutput("[Client/Error] type /help for a list of commands")
		if isCommand:

			if str(command[0]).lower() == self.cmdClear.name:
				os.system('cls' if os.name=='nt' else 'clear')

			elif str(command[0]).lower() == self.cmdHelp.name:
				self.guiHelper.printOutput("[Client/Info] Commands:")
				self.guiHelper.printOutput("----------------------------------------------------------")
				for command in self.commandList:
					self.guiHelper.printOutput(command.syntax + " : " + command.description)
				self.guiHelper.printOutput("----------------------------------------------------------")

			elif str(command[0]).lower() == self.cmdListChannel.name:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("022"))

			elif str(command[0]).lower() == self.cmdChangeChannel.name:
				newChannelName = None
				try:
					newChannelName = command[1]
				except IndexError:
					self.guiHelper.printOutput("[Client/Error] Syntax: " + self.cmdChangeChannel.syntax)
				if newChannelName != None:
					clientObject.channel = newChannelName
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023" + newChannelName))
					time.sleep(0.1)
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611" + newChannelName))
					time.sleep(0.1)
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("901"))

			elif str(command[0]).lower() == self.cmdSetName.name:
				newUsername = None
				try:
					newUsername = command[1]
				except IndexError:
					self.guiHelper.printOutput("[Client/Error] Syntax: " + self.cmdSetName.syntax)
				if newUsername != None:
					clientObject.username = newUsername
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031" + newUsername))

			elif str(command[0]).lower() == self.cmdDisconnect.name:
				clientObject.socketObject.shutdown(1)
				clientObject.socketObject.close()
			
			elif str(command[0]).lower() == self.cmdListClients.name:
				channel = None
				try:
					channel = command[1]
				except:
					self.guiHelper.printOutput("[Client/Error] Syntax: " + self.cmdListClients.syntax)
				if channel != None:
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611" + channel))

			elif str(command[0]).lower() == self.cmdKick.name:
				client = None
				try:
					client = command[1]
				except:
					self.guiHelper.printOutput("[Client/Error] Syntax: " + self.cmdKick.syntax)
				if client != None:
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411" + client))

			elif str(command[0]).lower() == self.cmdBan.name:
				client = None
				banTime = None
				try:
					client = command[1]
					banTime = command[2]
				except:
					self.guiHelper.printOutput("[Client/Error] Syntax: " + self.cmdBan.syntax)
				if client != None and banTime != None:
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("711" + client + " " + banTime))

			else:
				self.guiHelper.printOutput("[Client/Error] Unknown command: " + command[0])
				self.guiHelper.printOutput("[Client/Error] type /help for a list of commands")