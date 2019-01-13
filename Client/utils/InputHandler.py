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
			if str(command[0]).lower() == self.cmdClear.name:
				os.system('cls' if os.name=='nt' else 'clear')

			elif str(command[0]).lower() == self.cmdHelp.name:
				print("[Client/Info] Commands:")
				print("----------------------------------------------------------")
				for command in self.commandList:
					print(command.syntax + " : " + command.description)
				print("----------------------------------------------------------")

			elif str(command[0]).lower() == self.cmdlistChannel.name:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("022"))

			elif str(command[0]).lower() == self.cmdchangeChannel.name:
				newChannelName = None
				try:
					newChannelName = command[1]
				except IndexError:
					print("[Client/Error] Syntax: " + self.cmdchangeChannel.syntax)
				if newChannelName != None:
					clientObject.channel = newChannelName
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023" + newChannelName))

			elif str(command[0]).lower() == self.cmdSetName.name:
				newUsername = None
				try:
					newUsername = command[1]
					print(newUsername)
				except IndexError:
					print("[Client/Error] Syntax: " + self.cmdSetName.syntax)
				if newUsername != None:
					clientObject.username = newUsername
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031" + newUsername))
#TODO:/quit /disconnect that kind of thing
			else:
				print("[Client/Error] Unknown command: " + command[0])
				print("[Client/Error] type /help for a list of commands")