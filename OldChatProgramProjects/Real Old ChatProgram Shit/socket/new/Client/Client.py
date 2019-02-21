import socket
import threading
import json
import time
import struct

class Client:

	def __init__(self):
		self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.username = self.ask("Username:")
		self.password = self.ask("Password:")
		self.connect()
		threading.Thread(target=self.receiveData,args=[]).start()
		self.conn.send(bytes("001" + self.username + self.password, "utf8"))
		print("Requesting Channels")
		self.ask("wanna see channels")
		self.conn.send(bytes("002", "utf8"))


#helper def's
	def ask(self, question):
		return input(question + "\n")

	def connect(self):
		try:
			self.conn.connect(("127.0.0.1", 5000))
		except:
			print("could not connect to server")
			time.sleep(1)
			exit()

	def handlePacket(self, packetid, msg):
		if packetid == "001":
			if msg == "1":
				print("login was successfull")
			elif msg == "0":
				print("login was not sucesfull")
				self.conn.shutdown(socket.SHUT_RDWR)
				self.conn.close()
				time.sleep(1)
				self.__init__()
		elif packetid == "002":
			print("Channel:")
			print(msg.split(":")[1])
			self.ask("join channel?")
			selectedChannel = "channel1"
			self.conn.send(bytes("003" + selectedChannel, "utf8"))
			threading.Thread(target=self.WaitForChatMessage,args=[]).start()
			print("chatting begins")
		elif packetid == "003":
			print(msg)
#helper def's

#thread's
	def receiveData(self):
		while True:			
			data = self.conn.recv(8192)
			if len(data) > 0:
				data = str(data, "utf-8")
				packetid = data[:3]
				msg = data[3:]
				self.handlePacket(packetid, msg)

	def WaitForChatMessage(self):
		while True:
			msg = input()
			if "/" in msg:
				print("not working atm")
			else:
				self.conn.send(bytes("004" + self.username + ": "+ msg, "utf8"))
#thread's

Client()