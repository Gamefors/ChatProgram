from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611,E0401
from utils.ChannelManager import ChannelManager#pylint: disable=E0611,E0401
from utils.ClientManager import ClientManager#pylint: disable=E0611,E0401
from utils.FileHelper import FileHelper#pylint: disable=E0611,E0401
from utils.LogHelper import LogHelper#pylint: disable=E0611,E0401

from objects.Client import Client#pylint: disable=E0611,E0401

import socketserver, datetime, time

class ClientHandler(socketserver.BaseRequestHandler):
	
	appendClient = True
	tryRecv = False
	
	def importScripts(self):
		self.decEncHelper = DecodingEncodingHelper()
		self.channelManager = ChannelManager()
		self.clientManager = ClientManager()
		self.fileHelper = FileHelper()
		self.logHelper = LogHelper()
	
	#overwrite handle method	
	def handle(self):
		#imports
		self.importScripts()

		if self.appendClient:
			self.clientObject = Client(self.request, "*NONE*none*NONE+", self.channelManager.channelList[0], 0)
			self.clientObject.channelObject.clientList.append(self.clientObject)
			if len(self.fileHelper.readTXTFile("data/", "banList")) > 1:
				for client in self.fileHelper.readTXTFile("data/", "banList"):
					try:
						banTime = client.split(":")[1]
					except IndexError:
						var = None#pylint: disable=W0612
					if self.clientObject.ip + "\n" == client:
						self.logHelper.printAndWriteServerLog("[Server/Info] " + self.clientObject.ip + ":" + str(self.clientObject.port) + " is permanantly banned on the server")
						self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405[Client/Info] You are permanantly banned on this server"))
						self.clientObject.socketObject.close()
						self.appendClient = False
					elif self.clientObject.ip + ":" + banTime == client:
						currentTimeStamp = datetime.datetime.now().timestamp()
						banTime = banTime[:-1]
						if (currentTimeStamp > float(banTime)):
							self.fileHelper.removeClientFromBanList(self.clientObject.ip)
							self.clientManager.addClient(self.clientObject)
							self.logHelper.printAndWriteServerLog("[Server/Info] " + str(self.clientObject.ip) + " connected to the server")
							self.appendClient = False
							self.tryRecv = True
						else:
							self.logHelper.printAndWriteServerLog("[Server/Info] " + self.clientObject.ip + ":" + str(self.clientObject.port) + " is temporary banned on the server. Remaining Time: " +  str(int((float(banTime) - currentTimeStamp)/60)) + "Minutes")
							self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("405[Client/Info] You are temporary banned on this server. Remaining Time: " + str(int((float(banTime) - currentTimeStamp)/60)) + "Minutes"))
							self.channelManager.removeChannelMember(self.clientObject.channelObject ,self.clientObject)
							self.clientObject.socketObject.close()
							self.appendClient = False
							break
					elif "BanList:\n" == client:
						var = None
					else:
						self.clientManager.addClient(self.clientObject)
						self.logHelper.printAndWriteServerLog("[Server/Info] " + str(self.clientObject.ip) + " connected to the server.")
						self.appendClient = False
						self.tryRecv = True
			else:
				self.clientManager.addClient(self.clientObject)
				self.logHelper.printAndWriteServerLog("[Server/Info] " + str(self.clientObject.ip) + " connected to the server.")
				self.appendClient = False
				self.tryRecv = True	
		
		if self.tryRecv:
			try:
				self.data = self.decEncHelper.bytesToString(self.clientObject.socketObject.recv(1024))
				self.handleRequest(self.data, self.clientObject)
			except:
				for clientObjectInList in self.clientManager.clientList:
								if clientObjectInList != self.clientObject:
									if self.channelManager.channelContains(clientObjectInList, self.clientObject.channelObject.name):
										clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("811[Client/Info] " + self.clientObject.username + " quit."))
				self.logHelper.printAndWriteServerLog("[Server/Error] " + str(self.clientObject.ip) + " Disconnected")
				self.clientManager.removeClient(self.clientObject)
				self.channelManager.removeChannelMember(self.clientObject.channelObject ,self.clientObject)
	
	def handleRequest(self, request, clientObject):
		
		requestId = request[:3]
		requestdata = request[3:]

		if requestId == "001":#chatting
			self.logHelper.printAndWriteChannelLog(clientObject.channelObject.name,"[Server/Info][" + clientObject.channelObject.name + "] " + clientObject.ip + " " + clientObject.username + " : " + requestdata)	
			for clientObjectFromList in self.clientManager.clientList:
				if clientObjectFromList.channelObject.name == clientObject.channelObject.name:
					if clientObjectFromList != clientObject:					
						clientObjectFromList.socketObject.sendall(self.decEncHelper.stringToBytes("001" + clientObject.username + " : " + requestdata))

		elif requestId == "011":#get client informations
			self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " sent client informations.")
			self.clientManager.updateClientUsername(clientObject, requestdata)
			for clientObjectInList in self.clientManager.clientList:
								if clientObjectInList != clientObject:
									if self.channelManager.channelContains(clientObjectInList, "Welcome_Channel"):
										clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("811[Client/Info] " + clientObject.username + " joined your channel."))
		
		elif requestId == "611":#sent current clients in given channel
			self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " requested the clients from channel " + requestdata+ ".")
			for channel in self.channelManager.channelList:
				if channel.name == requestdata:
					if len(channel.clientList) < 1:
						self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611No clients are connected in this channel."))
					else:
						clientsInChannel = list()
						for client in channel.clientList:
							clientsInChannel.append(client.username)
						self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611" + str(clientsInChannel)))
						break
		
		elif requestId == "022":#send channel list  TODO: send more things like description acceslevel etc. but names work for now
			self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " requested channel.")
			channelNames = list()
			for channelObject in self.channelManager.channelList:
				channelNames.append(channelObject.name)
			self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("022" + str(channelNames)))

		elif requestId == "023":#changing channels
			if self.channelManager.channelExists(requestdata):
				if self.channelManager.channelContains(self.clientObject, requestdata):
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023[Client/Info] you are already in this channel."))
					self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " tried to join a channel which he is already part of.")					
				else:
					for channelObject in self.channelManager.channelList:
						if channelObject.name == requestdata:
							oldChannel = clientObject.channelObject.name
							self.channelManager.removeChannelMember(clientObject.channelObject, clientObject)
							clientObject.channelObject = channelObject
							self.channelManager.addChannelMember(channelObject, clientObject)
							for clientObjectInList in self.clientManager.clientList:
								if self.channelManager.channelContains(clientObject, requestdata):
									if clientObjectInList != clientObject:
										if clientObjectInList.channelObject.name == clientObject.channelObject.name:
											clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("811[Client/Info] " + clientObject.username + " joined your channel."))
										elif clientObjectInList.channelObject.name == oldChannel:
											clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("811[Client/Info] " + clientObject.username + " left your channel."))
							clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023[Client/Info] You succesfully changed channel."))
							self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " changed channel to : " + requestdata + ".")
							#print("oldchannel was " + oldChannel)
			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023[Client/Info] The channel you wanted to join doesn't exists."))
				self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " tried to join a channel that doesn't exists.")
			
		elif requestId == "031":#changing names
			clientObject.username = requestdata
			clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031[Client/Info] you succesfully changed your name."))
			self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : changed names.")

		elif requestId == "411":#kicking clients
			if self.clientManager.usernameExists(requestdata):
				if requestdata == self.clientObject.username:
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411[Client/Info] You can't kick yourself."))
				else:
					for clientObjectInList in self.clientManager.clientList:
							if clientObjectInList.username == requestdata:
								clientObjectInList.socketObject.sendall(self.decEncHelper.stringToBytes("402[Client/Info] You got kicked by: " + self.clientObject.username))
								clientObjectInList.socketObject.close()
								time.sleep(0.1)
								self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " kicked : " + requestdata)
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
								self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " kicked : " + requestdata)
								clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411[Client/Info] You sucessfully kicked: " + requestdata))
								break
			
			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("411[Client/Info] Username or ip doesnt exists on the server."))

		else: #any other requestId
			if len(requestId) == 0:
				raise SystemExit()
			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("401[Client/Error] Unknown request ID"))
				self.logHelper.printAndWriteServerLog("[Server/Error] " + clientObject.ip + " sent unknown request ID")
		
		self.handle()