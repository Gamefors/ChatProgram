from utils.LoggingHelper import LoggingHelper#pylint: disable=E0611,E0401
from utils.FileHelper import FileHelper#pylint: disable=E0611,E0401
import socketserver, threading
class Clients:#TO_DO_DEPLETED:put in own file maybe : clientAdministrationHelper.py?

	clientList = list()

	def removeClient(self, client, username):
		try:
			self.clientList.remove(dict({client : username}))
		except ValueError:
			var = None#pylint: disable=W0612

	def addClient(self, client, username):
		self.clientList.append(dict({client : username}))

class RequestHandler(socketserver.BaseRequestHandler):
	#variables
	appendClient = True

	clients = None

	client = None
	username = None

	#helper
	def BytesToString(self, bytes):
		return str(bytes, "utf-8")
	def StringToBytes(self, string):
		return bytes(string, "utf-8")

	def handle(self):
		logHelper = LoggingHelper()
		fileHelper = FileHelper()
		self.client = self.request
	
		self.clients = Clients()
		if self.appendClient:
			logHelper.printAndWriteServerLog("[Server/Info] " + str(self.client_address[0])+ ":" + str(self.client_address[1]) + " connected to the server")
			for clientInList in fileHelper.readTXTFile("data/", "banList"):
				clientInListString = clientInList.split(":")
				try:
					banTime = clientInListString[1]
				except IndexError:
					var = None#pylint: disable=W0612
				if self.client_address[0] + "\n" in clientInList:
					logHelper.printAndWriteServerLog("[Server/Info] " + str(self.client_address[0])+ ":" + str(self.client_address[1]) + " is permanantly banned on the server")
					self.client.sendall(self.StringToBytes("405[Client/Info] You are permanantly banned on this server"))
					self.client.close()
					self.appendClient = False
				elif self.client_address[0] + ":" + banTime in clientInList:#FIX_ME_DEPLETED:decrease banntime overtime
					logHelper.printAndWriteServerLog("[Server/Info] " + str(self.client_address[0])+ ":" + str(self.client_address[1]) + " is temporary banned on the server. Remaining Time: " + clientInListString[1] + "Minutes")
					self.client.sendall(self.StringToBytes("405[Client/Info] You are temporary banned on this server. Remaining Time: " + str(int(clientInListString[1])) + "Minutes"))
					self.client.close()
					self.appendClient = False
				else:
					self.clients.addClient(self.client, "None")
					self.appendClient = False
				

		try:
			self.data = self.BytesToString(self.client.recv(1024).strip())
			if len(self.data[6:]) == 0:
				logHelper.printAndWriteServerLog("[Server/Info] " + str(self.client_address[0])+ ":" + str(self.client_address[1]) + " sent client informations")
				self.handleRequest(self.data)
			else:
				logHelper.printAndWriteChannelLog("[Server/Channel/Info] " + str(self.client_address[0])+ ":" + str(self.client_address[1]) +" " +  self.data[3:])
				self.handleRequest(self.data)
		except:
			logHelper.printAndWriteServerLog("[Server/Error] " + str(self.client_address[0])+ ":" + str(self.client_address[1]) + " closed connection unexpectedly")
			self.clients.removeClient(self.client, self.username)


		

	def handleRequest(self, request):
		logHelper = LoggingHelper()		
		requestId = request[:3]
		requestdata = request[3:]
		if requestId == "001":		
			for client in self.clients.clientList:
				if client != dict({self.client : self.username}):					
					for key in client.keys():
						key.sendall(self.StringToBytes("001" + requestdata))
		elif requestId == "011":
			for client in self.clients.clientList:
				for key in client.keys():
					if client == dict({self.client : "None"}):
						if key.getpeername()[1] == self.client_address[1]:
							self.username = requestdata
							client[self.client] = requestdata	
						else:
							key.sendall(self.StringToBytes("411[Client/Error] You are already connected to this server"))
		else:
			self.client.sendall(self.StringToBytes("401[Client/Error] Unknown request ID"))
			logHelper.printAndWriteServerLog("[Server/Error] " + str(self.client_address[0])+ ":" + str(self.client_address[1]) + " sent unknown request ID")
		self.handle()