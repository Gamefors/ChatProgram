from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611
from utils.ServerHandler import ServerHandler#pylint: disable=E0611
from utils.InputHandler import InputHandler#pylint: disable=E0611
from utils.FileHelper import FileHelper#pylint: disable=E0611
from utils.GUIHelper import GUIHelper#pylint: disable=E0611

from objects.Client import ClientObject#pylint: disable=E0611

from tkinter import Label

from PyQt5 import QtWidgets, uic

import threading, socket, time, sys, os

class CustomDialog(QtWidgets.QDialog):
    
    def __init__(self):
        super(CustomDialog, self).__init__()
        self.customDialogWindow = uic.loadUi("resources/CustomDialog.ui", self)

    def getData(self):
        if self.customDialogWindow.exec_() == QtWidgets.QDialog.Accepted:
            username = self.customDialogWindow.username.text()
            password = self.customDialogWindow.password.text()
            return username + ":" + password
        else:
            return ":"

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

	def inizializeClient(self, username, password):
		self.clientObject = ClientObject(username, None, self.ipV4, self.port, "Welcome_Channel") 
		self.connected = False
		self.password = password

	def button(self):
		if self.mainWindow.statusButton.text() != "Offline":
			self.sendInput("/disconnect")
			self.mainWindow.statusButton.setText("Offline")
			self.mainWindow.output.clear()
			self.mainWindow.channelTree.clear()
			self.connected = False
		else:
			data = CustomDialog().getData()
			if data == ":":
				self.mainWindow.close()
			else:
				data = data.split(":")
				self.inizializeClient(data[0], data[1])
				self.tryConnect()

	def tryConnect(self):
		trys = 0
		while not self.connected:
			try:
				self.clientObject.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.clientObject.socketObject.connect((self.clientObject.ip, self.clientObject.port))
				threading.Thread(target=ServerHandler,args=[self.clientObject,self.mainWindow]).start()
				self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("011" + self.clientObject.username + ":" + self.password))
				self.connected = True
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
				self.output.append("you: " + message)
				try:
					
					self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("001" + message))
				except:
					self.connected = False
		else:
			self.guiHelper.printOutput("not connected")

	def __init__(self, username, password, mainWindow):
		#Imports
		self.mainWindow = mainWindow
		self.mainWindow.statusButton.clicked.connect(self.button)
		self.output = mainWindow.output
		self.importScripts()
		#Config
		self.setConfig()
		#Client initializations
		self.inizializeClient(username, password)
		#Client trying to establish a connection
		self.tryConnect()
		