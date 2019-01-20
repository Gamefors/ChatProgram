import os
#Client
class CommandHandler:
	CommandList = dict()
	def __init__(self):
		var = None

	#helper
	def BytesToString(self, bytes):
		return str(bytes, "utf-8") 
	def StringToBytes(self, string):
		return bytes(string, "utf-8")    	

	def handleCommand(self, command, username, clientSocket):
		command = command.split()
		if command[0] == "clear":
			os.system('cls' if os.name=='nt' else 'clear')
		elif command[0] == "setName":
			oldUsername = username
			newUsername = command[1]
			clientSocket.sendall(self.StringToBytes("021" + oldUsername + ":" + newUsername))

			var = None
		else:
			print("[Client/WIP] Commands are not implemented yet you issued command : " + command[0])