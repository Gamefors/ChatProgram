#Version 1.0.0
from utils.DecodingEncodingHelper import DecodingEncodingHelper
from utils.ChannelManager import ChannelManager
from utils.ClientManager import ClientManager
from utils.ClientHandler import ClientHandler
from utils.ServerThread import ServerThread
from utils.InputHandler import InputHandler
from utils.FileHelper import FileHelper
from utils.LogHelper import LogHelper

from objects.Channel import Channel

import socketserver, threading, socket, time

class Server:

	def importScripts(self):
		self.decEncHelper = DecodingEncodingHelper()
		self.channelManager = ChannelManager()
		self.clientManager = ClientManager()
		self.inputHandler = InputHandler(self.upTime)
		self.fileHelper = FileHelper()
		self.logHelper = LogHelper()

	def setConfig(self):
		config = self.fileHelper.getConfig("Server Config")
		self.port = config.port
		self.ipV4 = config.ip

	def inizializeChannel(self):
		self.welcomeChannel = Channel("Welcome_Channel", "welcome to the server", "No", 0, list())
		self.channel1 = Channel("Channel_1", "Description of channel 1", "No", 0, list())
		self.channel2 = Channel("Channel_2", "Description of channel 1", "No", 0, list())
		self.channel3 = Channel("Channel_3", "Description of channel 1", "No", 0, list())
		self.channelManager.addChannel(self.welcomeChannel)
		self.channelManager.addChannel(self.channel1)
		self.channelManager.addChannel(self.channel2)
		self.channelManager.addChannel(self.channel3)

	def inizializeServer(self):
		self.server = ServerThread((self.ipV4, self.port), ClientHandler)
		serverThread = threading.Thread(target=self.server.serve_forever)
		serverThread.daemon = True
		serverThread.start()
		self.logHelper.log("info" ,"Started server (version: " + self.fileHelper.getConfig("Version") + ") on ip: " + self.ipV4 + " port: " + str(self.port))

	def askForInput(self):
		while True:
			try:
				command = input()
			except KeyboardInterrupt:
				self.logHelper.log("info", "Gracefully stopping server...")
				if len(self.clientManager.clientList) < 1:
					self.logHelper.log("info", "Gracefully stopped server")
					break
				else:
					for clientObject in self.clientManager.clientList:
						clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("403"))
					self.logHelper.log("info", "Gracefully stopped server")
					break
			if str(command).startswith("/"):
				try:
					self.inputHandler.handleInput(str(command[1:]).lower())
				except IndexError:
					self.logHelper.log("info", "type /help for a list of commands.")	
			else:
				self.logHelper.log("info", "Commands always start with (/)")	

	def __init__(self):
		self.upTime = time.time()
		#Imports
		self.importScripts()
		#Config
		self.setConfig()
		#Channel initialization
		self.inizializeChannel()
		#Server initializations
		self.inizializeServer()
		#Console Input
		self.askForInput()
				
Server()