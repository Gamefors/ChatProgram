from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611,E0401
from utils.ClientManager import ClientManager#pylint: disable=E0611,E0401
from utils.LogHelper import LogHelper#pylint: disable=E0611,E0401
from utils.FileHelper import FileHelper#pylint: disable=E0611,E0401
from utils.ChannelManager import ChannelManager#pylint: disable=E0611,E0401

from objects.Client import Client#pylint: disable=E0611,E0401

import socketserver, datetime
class ClientHandler(socketserver.BaseRequestHandler):
	
	appendClient = True
	tryRecv = False
	#overwrite
	def handle(self):
		self.decEncHelper = DecodingEncodingHelper()
		self.logHelper = LogHelper()
		self.clientManager = ClientManager()
		self.fileHelper = FileHelper()
		self.channelManager = ChannelManager()
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
				else:
					#send something that client can filter out as "that channel doesnt exits"
					clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611[Client/Info] The channel doesn't exists."))
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
							self.channelManager.removeChannelMember(clientObject.channelObject, clientObject)
							clientObject.channelObject = channelObject
							self.channelManager.addChannelMember(channelObject, clientObject)
							clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023[Client/Info] You succesfully changed channel."))
							self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " changed channel to : " + requestdata)
			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("023[Client/Info] The channel you wanted to join doesn't exists."))
				self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : " + clientObject.username + " tried to join a channel that doesn't exists.")
			
		elif requestId == "031":#changing names
			clientObject.username = requestdata
			clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("031[Client/Info] you succesfully changed your name."))
			self.logHelper.printAndWriteServerLog("[Server/Info] " + clientObject.ip + " : changed names.")

		else: #any other requesId
			if len(requestId) == 0:
				raise SystemExit()
			else:
				clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("401[Client/Error] Unknown request ID"))
				self.logHelper.printAndWriteServerLog("[Server/Error] " + clientObject.ip + " sent unknown request ID")
		
		self.handle()