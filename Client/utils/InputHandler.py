from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611, E0401

from objects.Command import Command#pylint: disable=E0611, E0401

import os
class InputHandler:
	
	commandList = list()
	
	def __init__(self):
		#Imports
		self.decEncHelper = DecodingEncodingHelper()
		#Create Commands
		self.cmdClear = Command("Clear", "/clear", "NONE", "Clears your interpreter console.")
		self.cmdHelp = Command("Help", "/help", "NONE", "Shows a list of available commands.")
		self.cmdSetName = Command("SetName", "/setName <Name>", "NAME", "Changes your name to the specified one.")
		self.cmdlistChannel = Command("ListChannel", "/listChannel", "NONE", "Lists all Channel.")
		self.cmdchangeChannel = Command("ChangeChannel", "/changeChannel <Channel Name>", "ChannelName", "Enter the specified channel.")
		#Append Commands
		self.commandList.append(self.cmdClear)
		self.commandList.append(self.cmdHelp)
		self.commandList.append(self.cmdSetName)
		self.commandList.append(self.cmdlistChannel)
		self.commandList.append(self.cmdchangeChannel)	

	def handleInput(self, command, clientObject):
		isCommand = True
		command = command.split()
		try:
			var = command[0]
		except IndexError:
			isCommand = False
			print("[Client/Error] type /help for a list of commands")
		if isCommand:
			if command[0] == self.cmdClear.name:
				os.system('cls' if os.name=='nt' else 'clear')

			elif command[0] == self.cmdHelp.name:
				print("[Client/Info] Commands:")
				for command in self.commandList:
					print("[Client/Info] " + command.syntax + " : " + command.description)

			elif command[0] == self.cmdlistChannel.name:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("022"))

			elif command[0] == self.cmdchangeChannel.name:
				newChannelName = None
				try:
					newChannelName = command[1]
				except IndexError:
					print("[Client/Error] Syntax: " + self.cmdchangeChannel.syntax)
				if newChannelName != None:
					clientObject.channel = newChannelName
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023" + newChannelName))

			elif command[0] == self.cmdSetName.name:
				newUsername = None
				try:
					newUsername = command[1]
				except IndexError:
					print("[Client/Error] Syntax: " + self.cmdSetName.syntax)
				if newUsername != None:
					clientObject.username = newUsername
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031" + newUsername))

			else:
				print("[Client/Error] Unknown command: " + command[0])
				print("[Client/Error] type /help for a list of commands")