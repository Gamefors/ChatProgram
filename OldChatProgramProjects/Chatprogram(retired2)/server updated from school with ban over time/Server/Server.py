from utils.RequestHandler import RequestHandler#pylint: disable=E0611
from utils.InputHandler import InputHandler#pylint: disable=E0611
from utils.LoggingHelper import LoggingHelper#pylint: disable=E0611
from utils.ServerThread import ServerThread#pylint: disable=E0611
from utils.FileHelper import FileHelper#pylint: disable=E0611
import socketserver, threading, socket
class Server():

	inptHandler = None
	logHelper = None
	
	server = None

	ip = ""
	
	#config
	t = FileHelper().getConfig()[2]
	port = int(t[5:])

	#helper
	def BytesToString(self, bytes):
		return str(bytes, "utf-8")    
	def StringToBytes(self, string):
		return bytes(string, "utf-8")

	def __init__(self):		
		self.inptHandler = InputHandler()
		self.logHelper = LoggingHelper()

		self.ip = str(socket.gethostbyname(socket.gethostname()))
		self.server = ServerThread((self.ip, self.port), RequestHandler)
		
		serverThread = threading.Thread(target=self.server.serve_forever)
		serverThread.daemon = True
		serverThread.start()
		
		self.logHelper.printAndWriteServerLog("[Server/Info] Started on ip: " + str(self.ip) + " with port: " + str(self.port) + " in " + serverThread.name)
		self.askForInput()

	def askForInput(self):
		while True:
			try:
				message = input()
			except KeyboardInterrupt:
				self.logHelper.printAndWriteServerLog("[Server/Info] Gracefully stopping server...")
				from utils.RequestHandler import Clients#pylint: disable=E0611
				if len(Clients().clientList) < 1:
					self.logHelper.printAndWriteServerLog("[Server/Info] Gracefully stopped server")
					break
				else:
					for client in Clients().clientList:
						for key in client.keys():
							key.sendall(self.StringToBytes("403" + "[Client/Info] Server shut down"))
					self.logHelper.printAndWriteServerLog("[Server/Info] Gracefully stopped server")
					break

			
			if str(message).startswith("/"):
				self.inptHandler.handleInput(str(message[1:]))
			else:
				self.logHelper.printAndWriteServerLog("[Server/Error] Unknown command: (" + str(message) + ")")
				self.logHelper.printAndWriteServerLog("[Server/Error] type /help for a list of commands")
Server()