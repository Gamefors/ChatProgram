from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611, E0401

from objects.Command import Command#pylint: disable=E0611, E0401

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


	def createCommand(self, name, syntax, arguments, description):
		command = Command(name, syntax, arguments, description)
		self.commandList.append(command)
		return command

	def __init__(self):
		#Imports
		self.decEncHelper = DecodingEncodingHelper()
		#Create Commands
		self.initializeCommands()
	
	def handleInput(self, command, clientObject):
		isCommand = True
		command = command.split()
		try:
			var = command[0]#pylint: disable=W0612
		except IndexError:
			isCommand = False
			print("[Client/Error] type /help for a list of commands")
		if isCommand:

			if str(command[0]).lower() == self.cmdClear.name:
				os.system('cls' if os.name=='nt' else 'clear')

			elif str(command[0]).lower() == self.cmdHelp.name:
				print("[Client/Info] Commands:")
				print("----------------------------------------------------------")
				for command in self.commandList:
					print(command.syntax + " : " + command.description)
				print("----------------------------------------------------------")

			elif str(command[0]).lower() == self.cmdListChannel.name:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("022"))

			elif str(command[0]).lower() == self.cmdChangeChannel.name:
				newChannelName = None
				try:
					newChannelName = command[1]
				except IndexError:
					print("[Client/Error] Syntax: " + self.cmdChangeChannel.syntax)
				if newChannelName != None:
					clientObject.channel = newChannelName
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023" + newChannelName))
					time.sleep(0.1)
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611" + newChannelName))

			elif str(command[0]).lower() == self.cmdSetName.name:
				newUsername = None
				try:
					newUsername = command[1]
				except IndexError:
					print("[Client/Error] Syntax: " + self.cmdSetName.syntax)
				if newUsername != None:
					clientObject.username = newUsername
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031" + newUsername))

			elif str(command[0]).lower() == self.cmdDisconnect.name:
				print("[Client/Info] You disconnected from the server.")
				time.sleep(1.5)
				clientObject.socketObject.shutdown(1)
				clientObject.socketObject.close()
				quit()
			
			elif str(command[0]).lower() == self.cmdListClients.name:
				channel = None
				try:
					channel = command[1]
				except:
					print("[Client/Error] Syntax: " + self.cmdListClients.syntax)
				if channel != None:
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611" + channel))

			elif str(command[0]).lower() == self.cmdKick.name:
				client = None
				try:
					client = command[1]
				except:
					print("[Client/Error] Syntax: " + self.cmdKick.syntax)
				if client != None:
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411" + client))

			else:
				print("[Client/Error] Unknown command: " + command[0])
				print("[Client/Error] type /help for a list of commands")