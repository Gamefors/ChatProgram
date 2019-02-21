import threading
import json
import time
import random
class connectionuser:

	_server = None
	_requests = None

	connection = None
	address = None
	channel = None
	username = None

	def sendToClient(self, msg):
		try:
			self.connection.send(bytes(msg, "utf-8"))
		except:
			self._server.deleteConnection(self)

	def sendPacket(self, command, args):
		signNumber = str(random.randint(100000,10000000))
		header = " *start_server_request~" + signNumber + "~" + command + "*"
		during = " *during_server_request~" + signNumber + "~" + command + "*"
		footer = " *end_server_request~" + signNumber + "~" + command + "*"
		
		self.sendToClient(header)
		for x in args:
			time.sleep(0.05)
			if x is None:
				self.sendToClient(during + "---")
			else:
				self.sendToClient(during + str(x))
			time.sleep(0.05)
		self.sendToClient(footer)

	def __init__(self, conn, addr, server_, requests_):
		self.connection = conn
		self.address = addr
		self._server = server_
		self._requests = requests_
		threading.Thread(target=self.listen,args=[]).start()

	def returnResult(self, signNumber, command, result):
		header = " *start_server_result~" + str(signNumber) + "~" + command + "*"
		during = " *during_server_result~" + str(signNumber) + "~" + command + "*"
		footer = " *end_server_result~" + str(signNumber) + "~" + command + "*"

		#if "keepAlive" not in command:
		#	print(str(signNumber) + command + ":" + str(result))

		self.sendToClient(header)
		for x in result:
			time.sleep(0.05)
			self.sendToClient(during + str(x))
			time.sleep(0.05)
		self.sendToClient(footer)

	def listen(self):
		result = dict()

		while True:
			data = None
			try:
				data = str(self.connection.recv(1024), "utf-8")
			except:
				self._server.deleteConnection(self)
				break

			#Client Request Commands e.g tryLogin, tryRegister...
			if "*start_server_request~" in data:
				sign = data.split("~")[1]
				if sign not in result:
					result[sign] = list()
					continue
				continue
			elif "*during_server_request~" in data:
				result[data.split("~")[1]].append(data.split("*")[2])
				continue
			elif "*end_server_request~" in data:
				sign = data.split("~")[1]
				args = result[sign]

				if "tryLogin" in data:
					self._requests.tryLogin(args, self, sign)
				elif "tryRegister" in data: 
					self._requests.tryRegister(args, self, sign)
				elif "listChannels" in data: 
					self._requests.listChannels(args, self, sign)
				elif "logout" in data: 
					self._requests.logout(args, self, sign)
				elif "changeChannel" in data: 
					self._requests.changeChannel(args, self, sign)
				elif "keepAliveConnection" in data:
					self._requests.keepAliveConnection(args, self, sign)
				elif "listCurrentChannelClients" in data:
					self._requests.listCurrentChannelClients(args, self, sign)
				else:
					self._server.createlogUtil.printandwriteserverlog("Typo in Client Request Command: " + data)
				continue

			for connUsers in self._server.users:
				if connUsers == self:
					continue
				if connUsers.channel == self.channel:
					try:
						connUsers.sendToClient("[" + self.channel + "] [" + self.username + "] " + data)
					except:
						var = None