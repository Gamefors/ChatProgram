class ServerHandler:
	
	def __init__(self, clientObject):
		
		self.clientObject = clientObject

		self.easyRequestIds = ["001", "401", "411", "811", "023", "031", "411", "711"]

		self.kicked = False
		self.banned = False
		self.serverOffline = False

		while True:
			try:
				request = str(self.clientObject.socketObject.recv(1024), "utf-8")
				self.handleRequest(request)
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

	def handleRequest(self, request):
		requestId = request[:3]
		requestdata = request[3:]
		if requestId in self.easyRequestIds:
			print(requestdata)
		elif requestId == "402":
			print(requestdata)
			self.kicked = True
		elif requestId == "403":
			self.serverOffline = True
			print(requestdata)
		elif requestId == "022":
			tempList = requestdata.split(",")
			print("[Client/Info] Channels: ")
			for obj in tempList:
				obj = obj.replace("'"," ").strip("[]").strip()
				if self.clientObject.channel in obj:
					print(obj + "(you)")
				else:
					print(obj)		
		elif requestId == "611":
			if "exists" in requestdata:
				print(requestdata)
			else:
				print("[Client/Info] clients in this channel: ")
				tempList = requestdata.split(",")
				for obj in tempList:
					obj = obj.replace("'"," ").strip("[]").strip()
					if self.clientObject.username in obj:
						print(obj + "(you)")
					else:
						print(obj)	
		elif requestId == "405":
			print(requestdata)
			self.banned = True			
		elif len(requestId) == 0:
			raise SystemExit()
		else:
			print("[Client/Error] Server sent unknown requestId: " + requestId)