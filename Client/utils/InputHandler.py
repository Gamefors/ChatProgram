from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611, E0401

from objects.Command import Command#pylint: disable=E0611, E0401

import os,time
class InputHandler:
	
	commandList = list()
	
	def __init__(self):
		#Imports
		self.decEncHelper = DecodingEncodingHelper()
		#Create Commands
		self.cmdClear = Command("Clear", "/clear", "NONE", "Clears your interpreter console.")
		self.cmdHelp = Command("Help", "/help", "NONE", "Shows a list of available commands.")
		self.cmdSetName = Command("SetName", "/setName <Name>", "NAME", "Changes your name to the specified one.")
		self.cmdListChannel = Command("ListChannel", "/listChannel", "NONE", "Lists all Channel.")
		self.cmdChangeChannel = Command("ChangeChannel", "/changeChannel <Channel Name>", "ChannelName", "Enter the specified channel.")
		self.cmdDisconnect = Command("Disconnect", "/disconnect", "None", "Disconnects you from the server.")
		self.cmdListClients = Command("ListClients", "/listClients <Channel Name>", "Channel Name", "Shows you a list of clients connected to the specified channel.")
		#Append Commands
		self.commandList.append(self.cmdClear)
		self.commandList.append(self.cmdHelp)
		self.commandList.append(self.cmdSetName)
		self.commandList.append(self.cmdListChannel)
		self.commandList.append(self.cmdChangeChannel)	
		self.commandList.append(self.cmdDisconnect)
		self.commandList.append(self.cmdListClients)	

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

			elif str(command[0]).lower() == self.cmdSetName.name:
				newUsername = None
				try:
					newUsername = command[1]
				except IndexError:
					print("[Client/Error] Syntax: " + self.cmdSetName.syntax)
				if newUsername != None:
					if "exists" in newUsername:
						print("[Client/Error] blacklisted word in username.")
					else:
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

			else:
				print("[Client/Error] Unknown command: " + command[0])
				print("[Client/Error] type /help for a list of commands")