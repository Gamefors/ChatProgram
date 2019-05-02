from utils.GUIHelper import GUIHelper#pylint: disable=E0611, E0401
class ServerHandler:
	
	def __init__(self, clientObject):
		
		self.guiHelper = GUIHelper()

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
					self.guiHelper.printOutput("[Client/Info] Press enter to quit")
					raise SystemExit()
				elif self.banned:
					self.guiHelper.printOutput("[Client/Info] Press enter to quit")
					raise SystemExit()
				elif self.serverOffline:
					self.guiHelper.printOutput("[Client/Info] Press enter to quit")
					raise SystemExit()
				else:
					self.guiHelper.printOutput("[Client/ERROR] Server closed connection unexpectedly")
					self.guiHelper.printOutput("[Client/Info] Press enter to quit")
					raise SystemExit()

	def handleRequest(self, request):
		requestId = request[:3]
		requestdata = request[3:]
		if requestId in self.easyRequestIds:
			self.guiHelper.printOutput(requestdata)
		elif requestId == "402":
			self.guiHelper.printOutput(requestdata)
			self.kicked = True
		elif requestId == "403":
			self.serverOffline = True
			self.guiHelper.printOutput(requestdata)
		elif requestId == "022":
			count = 0
			channelNames = list()
			cahnnelDescriptions = list()
			channelPasswords = list()
			channelAccessLevels = list()
			channelAttributes = requestdata.split(":")
			self.guiHelper.printOutput("[Client/Info] Channels: ")
			for attributeList in channelAttributes:
				lenght = len(attributeList)
				attributes = attributeList.split(",")
				for attribute in attributes:		
					attribute = attribute.replace("'"," ").strip("[]").strip()
					print(attribute)
					#channelNames.append(item)
			for name in channelNames:
				print(name + " Desc: " + cahnnelDescriptions[count] + " PW: " + channelPasswords[count] + " AccessLevel: " + channelAccessLevels[count])
				count = count + 1
		elif requestId == "611":
			if "exists" in requestdata:
				self.guiHelper.printOutput(requestdata)
			else:
				self.guiHelper.printOutput("[Client/Info] clients in this channel: ")
				tempList = requestdata.split(",")
				for obj in tempList:
					obj = obj.replace("'"," ").strip("[]").strip()
					if self.clientObject.username in obj:
						self.guiHelper.printOutput(obj + "(you)")
					else:
						self.guiHelper.printOutput(obj)	
		elif requestId == "405":
			self.guiHelper.printOutput(requestdata)
			self.banned = True			
		elif len(requestId) == 0:
			raise SystemExit()
		else:
			self.guiHelper.printOutput("[Client/Error] Server sent unknown requestId: " + requestId)