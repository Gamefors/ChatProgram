from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611,E0401
from utils.ChannelManager import ChannelManager#pylint: disable=E0611,E0401
from utils.ClientManager import ClientManager#pylint: disable=E0611,E0401
from utils.MysqlHelper import MysqlHelper#pylint: disable=E0611,E0401
from utils.FileHelper import FileHelper#pylint: disable=E0611,E0401
from utils.LogHelper import LogHelper#pylint: disable=E0611,E0401
from objects.Client import Client#pylint: disable=E0611,E0401
import socketserver, datetime, time
class ClientHandler(socketserver.BaseRequestHandler):
	appendClient = True
	tryRecv = False
	loggedIn = False
	def handle(self):#overwrite TODO: find a way to import script only once not once per handle call
		self.decEncHelper = DecodingEncodingHelper()
		self.channelManager = ChannelManager()
		self.clientManager = ClientManager()
		self.mysqlHelper = MysqlHelper()
		self.fileHelper = FileHelper()
		self.logHelper = LogHelper()

		if self.appendClient:
			self.clientObject = Client(self.request, "*NOT_ASSIGNED*", "*NOT_ASSIGNED*", "*NOT_ASSIGNED*")
			if len(self.fileHelper.readTXTFile("data/", "banList")) > 1:
				for client in self.fileHelper.readTXTFile("data/", "banList"):
					try:
						banTime = client.split(":")[1]
					except IndexError:
						var = None#pylint: disable=W0612
					if self.clientObject.ip + "\n" == client:
						self.logHelper.log("info", self.clientObject.ip + ":" + str(self.clientObject.port) + " is permanantly banned on the server")
						self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405[Client/Info] You are permanantly banned on this server"))
						self.clientObject.socketObject.close()
						self.appendClient = False
					elif self.clientObject.ip + ":" + banTime == client:
						currentTimeStamp = datetime.datetime.now().timestamp()
						banTime = banTime[:-1]
						if (currentTimeStamp > float(banTime)):
							self.fileHelper.removeClientFromBanList(self.clientObject.ip)
							self.clientManager.addClient(self.clientObject)
							self.logHelper.log("info", str(self.clientObject.ip) + ":" + str(self.clientObject.port) + " connected to the server")
							self.appendClient = False
							self.tryRecv = True
						else:
							self.logHelper.log("info", self.clientObject.ip + ":" + str(self.clientObject.port) + " is temporary banned on the server. Remaining Time: " +  str(int((float(banTime) - currentTimeStamp)/60)) + "Minutes")
							self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405[Client/Info] You are temporary banned on this server. Remaining Time: " + str(int((float(banTime) - currentTimeStamp)/60)) + " Minutes"))
							self.channelManager.removeChannelMember(self.clientObject.channelObject ,self.clientObject)
							self.clientObject.socketObject.close()
							self.appendClient = False
							break
					elif "BanList:\n" == client:
						var = None
					else:
						self.clientManager.addClient(self.clientObject)
						self.logHelper.log("info", str(self.clientObject.ip) + ":" + str(self.clientObject.port) + " connected to the server.")
						self.appendClient = False
						self.tryRecv = True
			else:
				self.clientManager.addClient(self.clientObject)
				self.logHelper.log("info" ,str(self.clientObject.ip) + ":" + str(self.clientObject.port) + " connected to the server.")
				self.appendClient = False
				self.tryRecv = True	
		
		if self.tryRecv:
			try:
				self.data = self.decEncHelper.bytesToString(self.clientObject.socketObject.recv(1024))
				self.handleRequest(self.data, self.clientObject)
			except:
				for clientObjectInList in self.clientManager.clientList:
								if clientObjectInList != self.clientObject:
									if self.loggedIn:
										if self.channelManager.channelContains(clientObjectInList, self.clientObject.channelObject.name):
											clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("811[Client/Info] " + self.clientObject.username + " quit."))
				self.logHelper.log("info", self.clientObject.ip + ":" + str(self.clientObject.port) + " Disconnected")
				self.mysqlHelper.logoutAccount(self.clientObject)
				self.clientManager.removeClient(self.clientObject)
				if self.loggedIn:
					self.channelManager.removeChannelMember(self.clientObject.channelObject ,self.clientObject)
	
	def handleRequest(self, request, clientObject):
		
		requestId = request[:3]
		requestdata = request[3:]

		if requestId == "001":#chatting
			self.logHelper.channelLog("info", clientObject.channelObject.name, clientObject.ip + ":" + str(clientObject.port) + " [" + clientObject.rank + "]" + clientObject.username + " : " + requestdata)	
			for clientObjectFromList in self.clientManager.clientList:
				if clientObjectFromList.channelObject.name == clientObject.channelObject.name:
					if clientObjectFromList != clientObject:
						clientObjectFromList.socketObject.sendall(self.decEncHelper.stringToBytes("001[" + clientObject.rank + "]" + clientObject.username + " : " + requestdata))

		elif requestId == "011":#try logging in
			requestdata = requestdata.split(":")
			self.logHelper.log("info", str(self.clientObject.ip) + ":" + str(self.clientObject.port) + " tried logging in.")
			self.clientManager.updateClientUsername(clientObject, requestdata[0])
			if self.mysqlHelper.tryLogin(clientObject, requestdata[1]):
				self.loggedIn = True
				self.clientObject.channelObject = self.channelManager.channelList[0]
				self.clientObject.channelObject.clientList.append(self.clientObject)
				self.clientManager.updateClientRank(clientObject, self.mysqlHelper.getAccountRank(clientObject))
				for clientObjectInList in self.clientManager.clientList:
					if clientObjectInList != clientObject:
						if self.channelManager.channelContains(clientObjectInList, "Welcome_Channel"):
							clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("811[" + clientObject.rank + "]" + clientObject.username + " joined."))
				self.logHelper.log("info", str(self.clientObject.ip) + ":" + str(self.clientObject.port) + " logged in as " + clientObject.username + " succesfully.")
				for clientObjectInList in self.clientManager.clientList:
					if clientObjectInList != clientObject:
						if self.channelManager.channelContains(clientObjectInList, "Welcome_Channel"):
							clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("811[" + clientObject.rank + "]" + clientObject.username + " joined."))
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("903"))
			else:
				self.logHelper.log("info", str(self.clientObject.ip) + ":" + str(self.clientObject.port) + " couldn't log in.")
				self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("902"))
				self.clientObject.socketObject.close()

		elif requestId == "611":#sent current clients in given channel
			self.logHelper.log("info", str(self.clientObject.ip) + ":" + str(self.clientObject.port) + " " + clientObject.username + " requested the clients from channel " + requestdata + ".")
			for channel in self.channelManager.channelList:
				if channel.name == requestdata:
					if len(channel.clientList) < 1:
						self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611Empty"))
					else:
						clientsInChannel = list()
						for client in channel.clientList:
							clientsInChannel.append(client.username)
						self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611" + requestdata + ";" + str(clientsInChannel)))
						break
		
		elif requestId == "541":#sent client rank
			self.logHelper.log("info", clientObject.ip + " " + clientObject.username + " requested rank.")
			self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("541" + str(self.clientObject.rank)))

		elif requestId == "022":#channel request
			self.logHelper.log("info", clientObject.ip + " " + clientObject.username + " requested channel.")
			channelNames = list()
			channelDescriptions = list()
			channelPasswords = list()
			channelAccessLevels = list()
			for channelObject in self.channelManager.channelList:
				channelNames.append(channelObject.name)
				channelDescriptions.append(channelObject.description)
				channelPasswords.append(channelObject.password)
				channelAccessLevels.append(channelObject.accessLevel)
			self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("022" + str(channelNames) + ":" + str(channelDescriptions) + ":" + str(channelPasswords) + ":" + str(channelAccessLevels)))

		elif requestId == "023":#changing channels
			if self.channelManager.channelExists(requestdata):
				if self.channelManager.channelContains(self.clientObject, requestdata):
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023[Client/Info] you are already in this channel."))
					self.logHelper.log("info", clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " tried to join a channel which he is already part of.")					
				else:
					for channelObject in self.channelManager.channelList:
						if channelObject.name == requestdata:
							oldChannel = clientObject.channelObject.name
							self.channelManager.removeChannelMember(clientObject.channelObject, clientObject)
							clientObject.channelObject = channelObject
							self.channelManager.addChannelMember(channelObject, clientObject)
							clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023[Client/Info] You succesfully changed to "+ requestdata + "."))
							self.logHelper.log("info", clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " changed from " + oldChannel + " to " + requestdata + ".")
							for clientInList in self.clientManager.clientList:
								clientInList.socketObject.sendall(self.decEncHelper.stringToBytes("811"))

			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023[Client/Info] This Channel doesn't exists."))
				self.logHelper.log("info", clientObject.ip + " : " + clientObject.username + " tried to join a channel that doesn't exists.")

		elif requestId == "031":#changing namesFIXME: doesnt work with rank not tested witohut
			if self.clientManager.hasRank(clientObject, "admin"):
				self.fileHelper.removeClientRank(clientObject)
				clientObject.username = requestdata
				self.fileHelper.addClientRank(clientObject, "admin")
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031[Client/Info] you succesfully changed your name."))
				self.logHelper.log("info", clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " changed name.")
			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031[Client/Info] You don't have access to that command."))
				self.logHelper.log("info", clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " had no access to that command. Rank:(" + clientObject.rank.strip("\n") + ")")

		elif requestId == "411":#kicking clients
			if self.clientManager.hasRank(clientObject, "admin"):
				if self.clientManager.usernameExists(requestdata):
					if requestdata == self.clientObject.username:
						clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411[Client/Info] You can't kick yourself."))
					else:
						for clientObjectInList in self.clientManager.clientList:
								if clientObjectInList.username == requestdata:
									clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("402[Client/Info] You got kicked by: " + self.clientObject.username))
									clientObjectInList.socketObject.close()
									time.sleep(0.1)
									self.logHelper.log("info", clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " kicked : " + requestdata)
									clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411[Client/Info] You sucessfully kicked: " + requestdata))
									break

				elif self.clientManager.ipExists(requestdata):
					if requestdata == self.clientObject.ip:
						clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411[Client/Info] You can't kick yourself."))
					else:
						for clientObjectInList in self.clientManager.clientList:
								if clientObjectInList.ip == requestdata:
									clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("402[Client/Info] You got kicked by: " + self.clientObject.username))
									clientObjectInList.socketObject.close()
									self.logHelper.log("info", clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " kicked : " + requestdata)
									clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411[Client/Info] You sucessfully kicked: " + requestdata))
									break

				else:
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411[Client/Info] Username or ip doesnt exists on the server."))
			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031[Client/Info] You don't have access to that command."))
				self.logHelper.log("info", clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " had no access to that command. Rank:(" + clientObject.rank.strip("\n") + ")")

		elif requestId == "711":#banning clients
			if self.clientManager.hasRank(clientObject, "admin"):
				requestdata = requestdata.split()
				client = requestdata[0]
				banTime = requestdata[1]
				if self.clientManager.usernameExists(client):
					if client == self.clientObject.username:
						clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("711[Client/Info] You can't ban yourself."))
					else:
						for clientObjectInList in self.clientManager.clientList:
							if clientObjectInList.username == client:
								if banTime == 0:
									self.fileHelper.addClientToBanList(clientObjectInList.ip)
									self.logHelper.log("info", clientObjectInList.ip + ":" + str(clientObjectInList.port) + " " + clientObjectInList.username + " got permanantly banned by " + clientObject.username)						
									clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("711" + "[Client/Info] You got permanantly banned by " + clientObject.username))
									clientObjectInList.socketObject.close()
									clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("711[Client/Info] You sucessfully banned: " + clientObjectInList.username))
								else:
									currentTimeStamp = datetime.datetime.now().timestamp()
									self.fileHelper.addClientToBanList(clientObjectInList.ip + ":" + str(currentTimeStamp + int(banTime)*60))
									self.logHelper.log("info", clientObjectInList.ip + ":" + str(clientObjectInList.port) + " " + clientObjectInList.username + " got banned for " + str(banTime) + "minutes by " + clientObject.username)						
									clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("711" + "[Client/Info] You got banned for " + str(banTime) + "Minutes by " + clientObject.username))
									clientObjectInList.socketObject.close()
									clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("711[Client/Info] You sucessfully banned: " + clientObjectInList.username + " for " + str(banTime)))

				elif self.clientManager.ipExists(client):
					if client == self.clientObject.ip:
						clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("711[Client/Info] You can't ban yourself."))
					else:
						for clientObjectInList in self.clientManager.clientList:
								if clientObjectInList.ip == client:
									if banTime == 0:
										self.fileHelper.addClientToBanList(clientObjectInList.ip)
										self.logHelper.log("info", clientObjectInList.ip + ":" + str(clientObjectInList.port) + " " + clientObjectInList.username + " got permanantly banned by " + clientObject.username)						
										clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("711" + "[Client/Info] You got permanantly banned by " + clientObject.username))
										clientObjectInList.socketObject.close()
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("711[Client/Info] You sucessfully banned: " + clientObjectInList.username))
									else:
										currentTimeStamp = datetime.datetime.now().timestamp()
										self.fileHelper.addClientToBanList(clientObjectInList.ip + ":" + str(currentTimeStamp + int(banTime)*60))
										self.logHelper.log("info", clientObjectInList.ip + ":" + str(clientObjectInList.port) + " " + clientObjectInList.username + " got banned for " + str(banTime) + "minutes by " + clientObject.username)						
										clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("711" + "[Client/Info] You got banned for " + str(banTime) + "Minutes by " + clientObject.username))
										clientObjectInList.socketObject.close()
										clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("711[Client/Info] You sucessfully banned: " + clientObjectInList.username + " for " + str(banTime)))

				else:
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("711[Client/Info] Username or ip doesnt exists on the server."))
			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031[Client/Info] You don't have access to that command."))
				self.logHelper.log("info", clientObject.ip + ":" + str(clientObject.port) + " " + clientObject.username + " had no access to that command. Rank:(" + clientObject.rank.strip("\n") + ")")
		
		elif requestId == "901":#GUI get all channel with clients
			channelList = list()
			for channel in self.channelManager.channelList:
				memberList = list()
				for client in channel.clientList:
					if client.username == clientObject.username:
						memberList.append(client.username + "(you)")
					else:
						memberList.append(client.username)
				channelList.append(channel.name + ":" + str(memberList) + ";")
			clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("901" + str(channelList)))

		else: #any other requestId
			if len(requestId) == 0:
				raise SystemExit()
			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("401[Client/Error] Unknown request ID"))
				self.logHelper.log("error", clientObject.ip + ":" + str(clientObject.port) + " sent unknown request ID")
		
		self.handle()