import socket
import threading
import json
import time

from serverUtils.packetsUtils.packet import packet
from serverUtils.loggingUtils.createLogs import createLogs
from serverUtils.mysqlUtils.mysqlHelper import mysqlHelper
from serverUtils.commandsUtils.commands import commands
from serverUtils.fileUtils.readFiles import readFiles
from serverUtils.helper import helper

class Server:
#global declarations
	#list of connected clients(ip:port)
	clients = list()
	#list of users (ip:port | name | channel)
	users = list()
	#prefixes
	serverPrefix = "[Server] "
	#instancing of classes
	createLogsUtil = None
	helperUtils = None
	mysqlHelperUtil = None
	commandsUtil = None
	readFileUtil = None
	#last keep alive packet from ervery connection that needs to be kept alive
	lastKeepAlivePackets = dict()
#end of global declarations

#config section
	#the port the server should run on
	serverPort = 5000
	#max client ping in seconds
	maxClientPing = 15
#end of config section

	
	def __init__(self):
		#instancing of classes
		self.createLogsUtil = createLogs()
		self.mysqlHelperUtil = mysqlHelper(self)
		self.commandsUtil = commands(self)
		self.readFilesUtil = readFiles()

		self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.bind((socket.gethostbyname(socket.gethostname()), self.serverPort))

		#threading
		threading.Thread(target=self.listenForConnections,args=[]).start()
		threading.Thread(target=self.listenForPackets,args=[]).start()
		#threading.Thread(target=self.keepAliveRequestWorker,args=[]).start()
		#threading.Thread(target=self.interpreterInput,args=[]).start()

		#logging
		self.createLogsUtil.printandwriteserverlog(self.serverPrefix + "Started server on ip: " + socket.gethostbyname(socket.gethostname()) + ":" + str(self.serverPort))

		checkRegister = self.mysqlHelperUtil.checkRegister("jan")

	#Server helper
	def sendPacketToClient(self, packet_):
		packet_.receiver.send(packet_.compressedPacket)

	def listenForConnections(self):
		while True:
			self.connection.listen(1)
			client = self.connection.accept()
			banned = self.readFilesUtil.checkIfBanned(client[1][0])
			if banned:
				self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(client[1][0]) + ":" + str(client[1][1]) + " got kicked from server because of ban(pls compose new log message this is schelchtes englisch)")
				self.sendPacketToClient(packet("4", "banned", [""], client))
				client[0].shutdown(socket.SHUT_RDWR)
				client[0].close()
			else:
				self.clients.append(client)
				self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(client[1][0]) + ":" + str(client[1][1]) + " connected")

	def listenForPackets(self):
		while True:
			for client in self.clients:
				try:
					recvPacket = str(user[0].recv(8192), "utf-8")
					recvPacket = json.loads(recvPacket)
				except:
					self.users.remove(user)
					for IpAndName in self.loggedInUsers:
						if {} == IpAndName:
							var = None
						else:
							IpAndName.pop(str(user[1][0]))
					self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(user[1][0]) + ":" + str(user[1][1]) + " lost connection to server unexpectedly")
					
				if "0" == recvPacket['packetid']:
					containsIllegalCharachters = self.helperUtils.checkForIllegalCharachters(recvPacket['data'][0] + recvPacket['data'][1])
					if containsIllegalCharachters:
						self.sendPacketToClient(packet("20", "IllegalCharachters", ["ERROR:IllegalCharachters"], user))
					else:
						checkRegister = self.helperUtils.checkRegister(recvPacket['data'][0])
						if checkRegister:
							successfullyRegistered = self.mysqlHelperUtil.register(recvPacket['data'][0], recvPacket['data'][1], recvPacket['data'][2])
							if successfullyRegistered:
								self.sendPacketToClient(packet("0", "register", ["True"], user))
								self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(user[1][0]) + ":" + str(user[1][1]) + " registered a new User: " + recvPacket['data'][0])
							else:
								self.sendPacketToClient(packet("0", "register", ["False"], user))
						else:
							self.sendPacketToClient(packet("20", "userAllreadyExists", ["ERROR:userAllreadyExists"], user))
				else:
					print("unknown packet id received from " + str(user[1][0]) + ":" + str(user[1][1]))


Server()