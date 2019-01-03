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
		self.cmdlistChannel = Command("ListChannel", "/listChannel", "NONE", "Lists all Channel.")
		#Append Commands
		self.commandList.append(self.cmdClear)
		self.commandList.append(self.cmdHelp)
		self.commandList.append(self.cmdlistChannel)	

	def handleInput(self, command, clientObject):
		command = command.split()

		if command[0] == self.cmdClear.name:
			os.system('cls' if os.name=='nt' else 'clear')
		
		elif command[0] == self.cmdHelp.name:
			print("[Client/Info] Commands:")
			for command in self.commandList:
				print("[Client/Info] " + command.syntax + " : " + command.description)

		elif command[0] == self.cmdlistChannel.name:
			clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("022"))