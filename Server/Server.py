from utils.ClientHandler import ClientHandler#pylint: disable=E0611
from utils.ServerThread import ServerThread#pylint: disable=E0611
from utils.FileHelper import FileHelper#pylint: disable=E0611

from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611
from utils.ChannelManager import ChannelManager#pylint: disable=E0611
from utils.ClientManager import ClientManager#pylint: disable=E0611
from utils.InputHandler import InputHandler#pylint: disable=E0611
from utils.LogHelper import LogHelper#pylint: disable=E0611

from objects.Channel import Channel#pylint: disable=E0611

import socketserver, socket, threading

class Server:

	def __init__(self):
		#Imports
		self.decEncHelper = DecodingEncodingHelper()
		self.channelManager = ChannelManager()
		self.clientManager = ClientManager()
		self.inputHandler = InputHandler()
		self.fileHelper = FileHelper()
		self.logHelper = LogHelper()
		#Config
		Config = self.fileHelper.getConfig()
		self.port = Config.port
		try:
			self.ipV4 = socket.gethostbyname(socket.gethostname())
		except:
			self.ipV4 = "localhost"
		#Channel initialization
		self.welcomeChannel = Channel("Welcome_Channel", "welcome to the server", "No", 0, list())
		self.channel1 = Channel("Channel_1", "channel 1", "No", 0, list())
		self.channel2 = Channel("Channel_2", "channel 2", "No", 0, list())
		self.channel3 = Channel("Channel_3", "channel 3", "No", 0, list())
		self.channelManager.addChannel(self.welcomeChannel)
		self.channelManager.addChannel(self.channel1)
		self.channelManager.addChannel(self.channel2)
		self.channelManager.addChannel(self.channel3)
		#Server initializations
		self.server = ServerThread((self.ipV4, self.port), ClientHandler)
		serverThread = threading.Thread(target=self.server.serve_forever)
		serverThread.daemon = True
		serverThread.start()
		self.logHelper.printAndWriteServerLog("[Server/Info] Started on ip: " + self.ipV4 + " with port: " + str(self.port))
		#Console Input
		self.askForInput()

	def askForInput(self):
		while True:
			try:
				command = input()
			except KeyboardInterrupt:
				self.logHelper.printAndWriteServerLog("[Server/Info] Gracefully stopping server...")
				if len(self.clientManager.clientList) < 1:
					self.logHelper.printAndWriteServerLog("[Server/Info] Gracefully stopped server")
					break
				else:
					for clientObject in self.clientManager.clientList:
						clientObject.socketObject.sendall(self.decEncHelper.stringToBytes("403" + "[Client/Info] Server shut down"))
					self.logHelper.printAndWriteServerLog("[Server/Info] Gracefully stopped server")
					break
			if str(command).startswith("/"):
				self.inputHandler.handleInput(str(command[1:]).lower())
			else:
				self.logHelper.printAndWriteServerLog("[Server/Error] Commands always start with (/)")	
				
Server()