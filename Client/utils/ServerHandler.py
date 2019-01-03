class ServerHandler:
	def __init__(self, clientObject):
		self.clientObject = clientObject

		self.kicked = False
		self.banned = False
		self.serverOffline = False

		while True:
			try:
				request = str(self.clientObject.socketObject.recv(1024), "utf-8")
				self.handleRequest(request, self.clientObject)
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

	def handleRequest(self, request, clientObject):
		requestId = request[:3]
		requestdata = request[3:]
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

		elif requestId == "022":
			s = requestdata.split(",")
			for ch in s:
				print(ch)

		elif requestId == "023":
			print("[Client/Info] You succesfully changed channel.")

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
		elif len(requestId) == 0:
			raise SystemExit()
		else:
			print("[Client/Error] Unknown RequestID: " + requestId)
			raise SystemExit()