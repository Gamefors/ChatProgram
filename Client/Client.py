from utils.DecodingEncodingHelper import DecodingEncodingHelper
from utils.ServerHandler import ServerHandler
from utils.InputHandler import InputHandler
from utils.FileHelper import FileHelper
from utils.GUIHelper import GUIHelper

from objects.Client import ClientObject

from tkinter import Label

from PyQt5 import QtWidgets, uic

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

	def inizializeClient(self, username, password):
		self.clientObject = ClientObject(username, None, self.ipV4, self.port, "Welcome_Channel") 
		self.connected = False
		self.password = password

	def tryConnect(self):
		try:
			self.clientObject.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.clientObject.socketObject.connect((self.clientObject.ip, self.clientObject.port))
			threading.Thread(target=ServerHandler,args=[self.clientObject,self.windows]).start()
			self.clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("011" + self.clientObject.username + ":" + self.password))
			self.connected = True
		except:
			self.connected = False

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

	def __init__(self, username, password, windows):
		#Imports
		self.windows = windows
		self.output = self.windows[0].output
		self.importScripts()
		#Config
		self.setConfig()
		#Client initializations
		self.inizializeClient(username, password)
		#Client trying to establish a connection
		self.tryConnect()
		