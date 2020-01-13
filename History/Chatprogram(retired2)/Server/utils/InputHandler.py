from utils.LoggingHelper import LoggingHelper#pylint: disable=E0611,E0401
from utils.RequestHandler import Clients#pylint: disable=E0611,E0401
from utils.FileHelper import FileHelper#pylint: disable=E0611,E0401
import os
#Server
class InputHandler:

	CommandList = dict()

	fileHelper = None
	logHelper = None
	
	clients = None

	#helper
	def BytesToString(self, bytes):
		return str(bytes, "utf-8")    
	def StringToBytes(self, string):
		return bytes(string, "utf-8")

	def __init__(self):
		self.fileHelper = FileHelper()
		self.logHelper = LoggingHelper()
		self.clients = Clients()

	def handleInput(self, command):
		command = command.split()
		if command[0] == "clear":
			os.system('cls' if os.name=='nt' else 'clear')
		elif command[0] == "listClients":
			if len(self.clients.clientList) < 1:
				self.logHelper.printAndWriteServerLog("[Server/Error] No clients connected")
			else:
				self.logHelper.printAndWriteServerLog("[Server/Info] Connected clients:")
				for client in self.clients.clientList:
					for key in client.keys():
						self.logHelper.printAndWriteServerLog("[Server/Info] " + str(key.getpeername()) + " : " + str(client[key]))
		elif command[0] == "kick":
			try:
				user = command[1]			
				if len(self.clients.clientList) < 1:
					self.logHelper.printAndWriteServerLog("[Server/Error] No clients connected")
				else:
					for client in self.clients.clientList:
						for key in client.keys():
							if key.getpeername()[0] == user:
								self.logHelper.printAndWriteServerLog("[Server/Info] " + user + " : " + client[key] + " got kicked")						
								key.sendall(self.StringToBytes("402" + "[Client/Info] You got kicked by the console"))
								key.close()
							else:
								self.logHelper.printAndWriteServerLog("[Server/Error] No client with ip: " + user)
			except IndexError:
				self.logHelper.printAndWriteServerLog("[Server/Info] /kick <client>")
		elif command[0] == "ban":
			try:
				time = 0
				user = command[1]
				permanantly = True
				try:
					time = command[2]
				except:
					permanantly = True				
				if int(time) > 0:
						permanantly = False
				if len(self.clients.clientList) < 1:
					self.logHelper.printAndWriteServerLog("[Server/Error] No clients connected")
				else:
					for client in self.clients.clientList:
						for key in client.keys():
							if key.getpeername()[0] == user:
								if permanantly:
									self.fileHelper.addClientToBanList(user)
									self.logHelper.printAndWriteServerLog("[Server/Info] " + user + " : " + client[key] + " got permanantly banned")						
									key.sendall(self.StringToBytes("405" + "[Client/Info] You got permanantly banned by the console"))
									key.close()
								else:
									self.fileHelper.addClientToBanList(user+ ":" + time)
									self.logHelper.printAndWriteServerLog("[Server/Info] " + user + " : " + client[key] + " got banned for " + str(time) + "minutes")						
									key.sendall(self.StringToBytes("405" + "[Client/Info] You got banned for " + str(time) + "Minutes by the console"))
									key.close()				
							else:
								self.logHelper.printAndWriteServerLog("[Server/Error] No client with ip: " + user)			
			except IndexError:
				self.logHelper.printAndWriteServerLog("[Server/Info] /ban <client> <time>")
		else:
			self.logHelper.printAndWriteServerLog("[Server/Error] Unknown command: (" + str(command) + ")")
			self.logHelper.printAndWriteServerLog("[Server/Error] type /help for a list of commands")