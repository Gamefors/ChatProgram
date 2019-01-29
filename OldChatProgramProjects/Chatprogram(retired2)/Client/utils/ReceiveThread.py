import time, sys
class ReceiveThread:
	kicked = False
	banned = False
	serverOffline = False
	username = None


	def __init__(self , client, username):
		self.username = username
		while True:
			try:
				received = str(client.recv(1024), "utf-8")
				self.handleMessage(received)
			except:
				if self.kicked:
					print("[Client/Info] Press enter to quit")
					raise SystemExit()
				elif self.banned:
					print("[Client/Info] Press enter to quit")
					raise SystemExit()
				elif self.serverOffline:
					print("[Client/Info] Press enter to quit")
					raise SystemExit()
				else:
					print("[Client/ERROR] Server closed connection unexpectedly")
					print("[Client/Info] Press enter to quit")
					raise SystemExit()
				
		
	def handleMessage(self, message):
		requestId = message[:3]
		requestdata = message[3:]
		if requestId == "001":
			print(requestdata)
		elif requestId == "401":
			print(requestdata)
		elif requestId == "402":
			print(requestdata)
			self.kicked = True
		elif requestId == "403":
			self.serverOffline = True
			print(requestdata)
		elif requestId == "411":
			print(requestdata)
		elif requestId == "405":
			print(requestdata)
			self.banned = True
		elif requestId == "201":#confirmation of username change
			data = requestdata.split(":")
			if requestdata[0] == "201True":				
				self.username = requestdata[1]
				print("succesfully changed name")
				var = None	#if true then change username in client.py
			else:
				var = None # if false error or someting dont know		

		else:
			print("[Client/Error] from client Unknown request type")
			raise SystemExit()