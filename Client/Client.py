from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611
from utils.ServerHandler import ServerHandler#pylint: disable=E0611
from utils.InputHandler import InputHandler#pylint: disable=E0611
from utils.FileHelper import FileHelper#pylint: disable=E0611
from utils.GUIHelper import GUIHelper#pylint: disable=E0611

from objects.Client import ClientObject#pylint: disable=E0611

from tkinter import Label

import threading, socket, time, sys, os

class Client:

	def importScripts(self):
		self.decEncHelper = DecodingEncodingHelper()
		self.inputHandler = InputHandler(self.output)
		self.fileHelper = FileHelper(self.output)
		self.guiHelper = GUIHelper(self.output)

	def setConfig(self):
		Config = self.fileHelper.getConfig()
		self.ipV4 = Config.ip
		self.port = Config.port

	def inizializeClient(self, username):
		self.clientObject = ClientObject(username, None, self.ipV4, self.port, "Welcome_Channel") 
		self.connected = False

	def tryConnect(self):
		trys = 0
		while not self.connected:
			try:
				self.clientObject.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.clientObject.socketObject.connect((self.clientObject.ip, self.clientObject.port))
				threading.Thread(target=ServerHandler,args=[self.clientObject,self.output]).start()
				self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("011" + self.clientObject.username))
				time.sleep(0.1)
				self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("611Welcome_Channel"))
				self.connected = True
				self.guiHelper.printOutput("[Client/Info] You are now connected to the server.")	
			except:
				trys = trys + 1
				os.system('cls' if os.name=='nt' else 'clear')
				self.guiHelper.printOutput("[Client/Info] Attempting to connect to server with ip: " + self.clientObject.ip + ". Attempts: " + str(trys))
				time.sleep(5)

	def sendInput(self, message):
		if self.connected:
			if str(message).startswith("/"):
					self.inputHandler.handleInput(str(message[1:]), self.clientObject)
			else:
				self.output.append(message)
				try:
					
					self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("001" + message))
				except:
					self.connected = False
		else:
			self.guiHelper.printOutput("not connected")

#############################################################################################################
	def askForInput(self):
		while self.connected:			
			message = input()
			if str(message).startswith("/"):
				self.inputHandler.handleInput(str(message[1:]), self.clientObject)
			else:
				try:
					self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("001" + message))
				except:
					self.connected = False
##############################################################################################################

	def __init__(self, username, output):
		#Imports
		self.output = output
		self.importScripts()
		#Config
		self.setConfig()
		#Client initializations
		self.inizializeClient(username)
		#Client trying to establish a connection
		self.tryConnect()
		
		#Client Input
		#self.askForInput()



#Client("FromPyQt")