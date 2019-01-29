import socket
import threading
import time
import random
from utils.messaging import messaging
from utils.inputs import inputs
from utils.requests import requests
from utils.commands import commands
from datetime import datetime
class user:


	results = dict()
	#global declarations for class user
	#Utilities
	messageUtil = None
	inputsUtil = None
	requestsUtil = None
	commandsUtil = None
	#clientinformations
	username = None
	channel = None
	#client connection
	client = None
	#bools
	#client network informations
	adress = None
	ip = None
	port = None
	#end of global declarations for class user

	#constructor for class user
	def __init__(self):
		self.messageUtil = messaging(self)
		self.inputsUtil = inputs(self)
		self.requestsUtil = requests(self)
		self.commandsUtil = commands(self)

		self.openConn()

		self.requestsUtil.requestAction()
	#end of constructor for class user

	def openConn(self):
		self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.client.connect(("93.244.22.92", 5000))
		loopingThread = threading.Thread(target=self.startLooping, args=[])
		loopingThread.start()
		keepAliveConnectionThread = threading.Thread(target=self.sendKeepAliveConnection,args=[])
		keepAliveConnectionThread.start()

	def sendKeepAliveConnection(self):
		while True:
			time.sleep(5)
			result = self.executeServer("keepAliveConnection", [str(datetime.now().microsecond)])


	def startLooping(self):
		while True:
			data = str(self.client.recv(1024), "utf-8")

			if (" *start_server_result~") in data:
				self.results[data.split("~")[1]] = serverResult()
				continue
			elif (" *during_server_result~") in data:
				self.results[data.split("~")[1]].result.append(data.split("*")[2])
				continue
			elif (" *end_server_result~") in data:
				self.results[data.split("~")[1]].finished = True
				continue

			self.messageUtil.chatmessage(data)

	def sendData(self, msg):
		self.client.send(bytes(msg, "utf-8"))

	#tryLogin username, password, email | returns true or false
	#tryRegister username, password, email | returns true or false
	#listChannel | returns Channel as dict channelname:channeldescription
	#logout | returns True 
	#changeChannel channel | returns nothing
	#keepAliveConnection | returns ping
	#exitchannel | returns nothing
	#listCurrentChannelClients | returns active users in channel
	def executeServer(self, command, args):
		signNumber = str(random.randint(100000,10000000))
		header = " *start_server_request~" + signNumber + "~" + command + "*"
		during = " *during_server_request~" + signNumber + "~" + command + "*"
		footer = " *end_server_request~" + signNumber + "~" + command + "*"

		self.catchMessages = False
		self.sendData(header)

		for x in args:
			time.sleep(0.05)
			if x is None:
				self.sendData(during + "---")
			else:
				self.sendData(during + str(x))
			time.sleep(0.05)
		self.sendData(footer)

		result = list()
		sign = None

		while True:
			if signNumber in self.results and self.results[signNumber].finished:
				return self.results[signNumber].result

class serverResult:

	finished = False
	result = None

	def __init__(self):
		self.result = list()


user()


