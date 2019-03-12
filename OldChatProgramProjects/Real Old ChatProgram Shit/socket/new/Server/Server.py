import socket
import threading
import json
import time

from utilities.Connection import Connection

class Server:
	connections = dict()
	msgQueue = dict()
#config section
	#the port the server should run on
	serverPort = 5000
	#max client ping in seconds
	maxClientPing = 15
#end of config sectiona
	

	def __init__(self):
		self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.bind((socket.gethostbyname(socket.gethostname()), self.serverPort))
		self.connection.listen(1)


		print("Started server on ip: " + socket.gethostbyname(socket.gethostname()) + ":" + str(self.serverPort))

		threading.Thread(target=self.receiveConnections,args=[]).start()
		threading.Thread(target=self.receiveData,args=[]).start()
		threading.Thread(target=self.chatQueue,args=[]).start()


	def receiveConnections(self):
		while True:
			newConnection = self.connection.accept()
			print("accepted connection from: " + str(newConnection[1]))
			self.connections[newConnection[1][1]] = Connection(newConnection[0], newConnection[1])

	def receiveData(self):
		while True:
			for connPort in list(self.connections):
				chatMsg = self.connections[connPort].tryRecv()
				self.msgQueue[connPort] = chatMsg
	def chatQueue(self):
		while True:
			for connPort in list(self.msgQueue):
				for allConn in list(self.connections):
					if self.connections[allConn].channel == self.conenctions[connPort].channel:
						self.connections[allConn].connection.send(bytes("004" + self.msgQueue[connPort], "utf8"))
Server()	


