import socket
import threading
import json
import time

from serverUtils.packetsUtils.packet import packet
from serverUtils.loggingUtils.createLogs import createLogs
from serverUtils.mysqlUtils.mysqlHelper import mysqlHelper
from serverUtils.commandsUtils.commands import commands
from serverUtils.helper import helper
#packet_['packetid']
#packet_['command']
#packet_['receiver']
#packet_['data']

class server:

#global server declarations
	#list of conencted clients
	users = list()
	#list of loggedin in users 
	loggedInUsers = list()
	#prefixes
	serverPrefix = "[Server] "
	#server ip
	serverIp = None
	#server prot
	serverPort = None
	#max client ping
	maxClientPing = 15
	#instances of classes
	createLogsUtil = None
	helperUtils = None
	mysqlHelperUtil = None
	#last keep alive packet from ervery connection that needs to be kept alive
	lastKeepAlivePackets = dict()
	loggedIn = False


#server constructor 
	def __init__(self):

		self.helperUtils = helper()
		self.createLogsUtil = createLogs()
		self.mysqlHelperUtil = mysqlHelper(self)
		self.commandsUtil = commands(self)

		serverIp = "localhost"
		serverPort = 5000

		self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.bind((serverIp, serverPort))
		#threading
		threading.Thread(target=self.listenForConnections,args=[]).start()
		threading.Thread(target=self.listenForPackets,args=[]).start()
		threading.Thread(target=self.keepAliveRequestWorker,args=[]).start()
		threading.Thread(target=self.interpreterInput,args=[]).start()
		#logging
		self.createLogsUtil.printandwriteserverlog(self.serverPrefix + "Started server on ip: " + serverIp + ":" + str(serverPort))
	

#server helper
	def sendPacketToClient(self, packet_):
		packet_.receiver.send(packet_.compressedPacket)

#server threads19

	def listenForConnections(self):
		while True:
			self.connection.listen(1)
			client = self.connection.accept()
			if self.mysqlHelperUtil.isBanned(client[1][0]):
				self.sendPacketToClient(packet("4", "ban", ["True"], client))
				client[0].shutdown(socket.SHUT_RDWR)
				client[0].close()
			else:
				self.users.append(client)
				self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(client[1][0]) + ":" + str(client[1][1]) + " connected")

	def listenForPackets(self):
		while True:
			for user in self.users:
				try:
					packet_ = str(user[0].recv(8192), "utf-8")
					print(packet_)
					packet_ = json.loads(packet_)
				except:
					self.users.remove(user)
					for IpAndName in self.loggedInUsers:
						if {} == IpAndName:
							var = None
						else:
							IpAndName.pop(str(user[1][0]))
					self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(user[1][0]) + ":" + str(user[1][1]) + " lost connection to server unexpectedly")
					

				if "0" == packet_['packetid']:
					containsIllegalCharachters = self.helperUtils.checkForIllegalCharachters(packet_['data'][0] + packet_['data'][1])
					if containsIllegalCharachters:
						self.sendPacketToClient(packet("0", "register", ["False"], user))
					else: 
						success = self.mysqlHelperUtil.register(packet_['data'][0], packet_['data'][1], packet_['data'][2])
						if success:
							self.sendPacketToClient(packet("0", "register", ["True"], user))
							self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(user[1][0]) + ":" + str(user[1][1]) + " registered a new User: " + packet_['data'][0])
						else:
							self.sendPacketToClient(packet("0", "register", ["False"], user))
				elif "1" == packet_['packetid']:
					containsIllegalCharachters = self.helperUtils.checkForIllegalCharachters(packet_['data'][0] + packet_['data'][1])
					if containsIllegalCharachters:
						self.sendPacketToClient(packet("1", "login", ["False"], user))
						self.loggedIn = False
					else:

						#for loggedInUser in self.loggedInUsers:
						#	if {} == loggedInUser:
						#		self.loggedIn = False
						#		break
						#	for ip, loggedInUser1 in loggedInUser.items():
						#		print("test1.5")
						#		if loggedInUser1 == packet_['data'][0]:
						#			print("test2")
						#			self.sendPacketToClient(packet("1", "login", ["False"], user))
						#			self.loggedIn = True
						#		else:
						#			self.loggedIn = False


						#if self.loggedIn:
						#	print("the user is allready logged in")
						#else:
						success = self.mysqlHelperUtil.checkLogin(packet_['data'][0], packet_['data'][1])
						if success:
							self.mysqlHelperUtil.updateAddress(packet_['data'][0], str(user[1][0]))
							self.loggedInUsers.append({str(user[1][0]) : packet_['data'][0]})
							self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(user[1][0]) + ":" + str(user[1][1]) + " logged in as: " + packet_['data'][0])
							self.sendPacketToClient(packet("1", "login", ["True"], user))
						else:
							self.sendPacketToClient(packet("1", "login", ["False"], user))		
				
				elif "2" == packet_['packetid']:
					channels = self.mysqlHelperUtil.getChannels()
					self.sendPacketToClient(packet("2", "listChannels", [channels], user))
					self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(user[1][0]) + ":" + str(user[1][1]) + " requested channels")
				


				elif "3" == packet_['packetid']:
					channels = self.mysqlHelperUtil.getChannels()
					if packet_['data'][0] in channels:
						self.sendPacketToClient(packet("3", "changeChannel", ["True"], user))
						#send user join the channel to all other users in the channel
						#assign the user the channel he joined
						self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(user[1][0]) + ":" + str(user[1][1]) + " changed channel to " + packet_['data'][0])
					else:
						self.sendPacketToClient(packet("3", "changeChannel", ["False"], user))


				elif "4" == packet_['packetid']:
					var = None
				elif "5" == packet_['packetid']:
					var = None
				elif "6" == packet_['packetid']:
					var = None
				elif "7" == packet_['packetid']:
					if (time.time() - int(packet_['data'][0])) > self.maxClientPing:
						self.sendPacketToClient(packet("7", "keepAlivePackage", ["False"], user))
						self.users.remove(user)
						for IpAndName in self.loggedInUsers:
							IpAndName.pop(str(user[1][0]))
						user[0].shutdown(socket.SHUT_RDWR)
						user[0].close()
						self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(user[1][0]) + ":" + str(user[1][1]) + " timed out due to high ping")
					self.lastKeepAlivePackets[user[1]] = time.time()
				elif "10" == packet_['packetid']:
					for userToSendTheMessage in self.users:
						if userToSendTheMessage == user:
							print("user who sent the message cant be the receiver")
						else:
							#check if users are in the same channel
							self.sendPacketToClient(packet("10", "chatMsg", [packet_['data']], userToSendTheMessage))
				else:
					print("unknown packet received from client" + str(user[1][0]) + ":" + str(user[1][1]))

	def keepAliveRequestWorker(self):
		while True:
			time.sleep(3)
			for user in self.users:
				if user[1] in self.lastKeepAlivePackets and (time.time() - self.lastKeepAlivePackets[user[1]]) > 8:
					self.users.remove(user)
					for IpAndName in self.loggedInUsers:
						IpAndName.pop(str(user[1][0]))
					user[0].shutdown(socket.SHUT_RDWR)
					user[0].close()
					self.createLogsUtil.printandwriteserverlog(self.serverPrefix + str(user[1][0]) + ":" + str(user[1][1]) + " timed out")
				else:
					self.sendPacketToClient(packet("7", "keepAlivePackage", ["True"], user))

	def interpreterInput(self):
		while True:
			command = input()
			
			if command.startswith("/"):
				commandName = command.split(" ")[0].replace("/", "") if " " in command else command.replace("/", "")

				if commandName in self.commandsUtil.availableCommands:
					args = list()
					if " " in command:
						for arg in command.split(" "):
							if not arg.startswith("/"):
								args.append(arg)

					if self.commandsUtil.availableCommands[commandName].correctArgs(args):
						self.commandsUtil.availableCommands[commandName].execute(args)
					else:
						print("Please use the following syntax: " + self.commandsUtil.availableCommands[commandName].syntax)
				else:
					self.commandsUtil.availableCommands["help"].execute([])
			else:
				self.commandsUtil.availableCommands["help"].execute([])

#initialize server
server()