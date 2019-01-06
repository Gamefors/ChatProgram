from utils.ServerHandler import ServerHandler#pylint: disable=E0611
from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611
from utils.InputHandler import InputHandler#pylint: disable=E0611

from objects.Client import ClientObject#pylint: disable=E0611

import threading, socket, time, sys, os

class Client:

	def __init__(self):
		self.decEncHelper = DecodingEncodingHelper()
		self.inputHandler = InputHandler()
		username = input("Username:")

		self.clientObject = ClientObject(username, None, "192.168.0.100", 5000, "first_channel_is_managed_by_server") 
		self.connected = False

		self.tryConnect()
		self.askForInput()

	def tryConnect(self):
		trys = 0
		while not self.connected:
			try:
				self.clientObject.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.clientObject.socketObject.connect((self.clientObject.ip, self.clientObject.port))
				threading.Thread(target=ServerHandler,args=[self.clientObject]).start()
				self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("011" + self.clientObject.username))
				self.connected = True
				print("[Client/Info] You are now connected to the server.")
			except:
				trys = trys + 1
				os.system('cls' if os.name=='nt' else 'clear')
				print("[Client/Info] Attempting to connect to server. Attempts: " + str(trys))
				time.sleep(5)

	def askForInput(self):
		while self.connected:			
			message = input()
			if str(message).startswith("/"):
				self.inputHandler.handleInput(str(message[1:]).lower(), self.clientObject)
			else:
				try:
					self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("001" + message))
				except:
					self.connected = False

Client()