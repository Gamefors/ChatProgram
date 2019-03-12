import json
import random
import threading
class packet:

	data = None

	uniqueId = random.randint(1,10000000)
	packetName = None
	payload = None
	reciever = None

	result = None

	def __init__(self, packetName_, payload_, reciever_):
		self.packetName = packetName_
		self.payload = payload_
		self.reciever = reciever_
		self.serializePacket()

	def serializePacket():
		self.data = bytes(json.dumps('{ "header" : [ {"reciever" : "' + self.reciever + '", "packetname" : "' + self.packetName + '", "uniqueId" : "' + self.uniqueId + '"} ], "payload" : [ { "data" : "' + json.dumps(self.payload) + '" } ] }'), "utf-8")


class packets:

	_packets = dict()
	_user = None

	def __init__(self, user_):
		self._user = user_
		read = threading.Thread(target=self.read,args=[])
		read.start()

	def read():
		while True:
			try:
				data = self._user.recv(1024)
				data = str(data, "utf-8")
				data = json.loads(data)

				print(data['payload'])

			except:
				print("Error!")

	def send():





