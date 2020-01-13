import socket
import threading
import time
import random
import sys
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
	packetsUtil = None
	#clientinformations
	username = None
	channel = None
	#client connection
	client = None
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

	#helper
	def informUser(self, msg):
		print(msg)
	#end of helper

	def openConn(self):
		self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.client.connect(("192.168.2.109", 5000))
		self.packetsUtil = packets(self.client)
		keepAliveConnectionThread = threading.Thread(target=self.sendKeepAliveConnection,args=[])
		keepAliveConnectionThread.start()

	def sendKeepAliveConnection(self):
		while True:
			time.sleep(5)
			result = self.executeServer("keepAliveConnection", [str(datetime.now().microsecond)])


	def startLooping(self):
		while True:
			try:
			    data = str(self.client.recv(1024), "utf-8")
			except:
				break
				quit()
				exit()

			if (" *start_server_result~") in data:
				self.results[data.split("~")[1]] = serverResult()
				continue
			elif (" *during_server_result~") in data:
				self.results[data.split("~")[1]].result.append(data.split("*")[2])
				continue
			elif (" *end_server_result~") in data:
				self.results[data.split("~")[1]].finished = True
				sign = data.split("~")[1]
				command = data.split("~")[2].split("*")[0]
				




				#Kriegt das ende nicht?
				#if "keepAlive" not in command:
				#	print(str(sign) + str(self.results[data.split("~")[1]].result))

				#chekc if sign is really smaller than 0
				if "changeChannel" in command and int(sign) < 0:
					self.requestsUtil.requestChangeChannel()
				elif "ban" in command and int(sign) < 0:
					print("You were banned")
					time.sleep(2)
					quit()
					exit()

				continue

			self.messageUtil.chatmessage(data)

	def sendData(self, msg):
		try:
			self.client.send(bytes(msg, "utf-8"))
		except:
			quit()
			exit()


	#tryLogin username, password, email | returns true or false
	#tryRegister username, password, email | returns true or false

	#listChannel | returns Channel as dict channelname:channeldescription
	#logout | returns True 
	#changeChannel channel | returns nothing
	#keepAliveConnection | returns ping
	#exitchannel | returns nothing
	#listCurrentChannelClients | returns active users in channel
	#kick | returns True
	#ban | returns True
	def executeServer(self, command, args):
		signNumber = str(random.randint(100000,10000000))
		header = " *start_server_request~" + signNumber + "~" + command + "*"
		during = " *during_server_request~" + signNumber + "~" + command + "*"
		footer = " *end_server_request~" + signNumber + "~" + command + "*"

		self.sendData(header)

		for x in args:
			time.sleep(0.05)
			if x is None:
				self.sendData(during + "---")
			else:
				self.sendData(during + str(x))
			time.sleep(0.05)
		self.sendData(footer)

		while True:
			if str(signNumber) in self.results and self.results[str(signNumber)].finished:
				return self.results[str(signNumber)].result

class serverResult:

	finished = False
	result = None

	def __init__(self):
		self.result = list()


user()


