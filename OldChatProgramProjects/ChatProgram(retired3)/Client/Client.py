from utils.CommandHandler import CommandHandler#pylint: disable=E0611
from utils.ReceiveThread import ReceiveThread#pylint: disable=E0611
import threading, socket, time, sys, os
class Client:
	#variables
	ip = "192.168.0.105"
	port = 5000
	client = None
	cmdHandler = None
	username = None
	connected = False

	#helper
	def BytesToString(self, bytes):
		return str(bytes, "utf-8") 
	def StringToBytes(self, string):
		return bytes(string, "utf-8")    	

	def __init__(self):
		self.username = input("Username:")
		self.cmdHandler = CommandHandler()
		self.tryConnect()
		self.askForInput()

	def tryConnect(self):
		trys = 0
		while not self.connected:
			try:
				self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.client.connect((self.ip, self.port))
				threading.Thread(target=ReceiveThread,args=[self.client]).start()
				self.client.sendall(self.StringToBytes("011" + self.username))
				self.connected = True
			except:
				trys = trys + 1
				os.system('cls' if os.name=='nt' else 'clear')
				print("Connection attempt:" + str(trys))

	def askForInput(self):
		while self.connected:			
			message = input()
			if str(message).startswith("/"):
				self.cmdHandler.handleCommand(message)
			else:
				try:
					self.client.sendall(self.StringToBytes("001" + self.username + " : " + message))
				except:
					self.connected = False
					#self.tryConnect():reconnect when not kicked or banned	ask on first connection if banend
Client()

	