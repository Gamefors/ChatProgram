from utils.GUIHelper import GUIHelper#pylint: disable=E0611, E0401
from utils.DecodingEncodingHelper import DecodingEncodingHelper#pylint: disable=E0611, E0401
from PyQt5.QtWidgets import QTreeWidgetItem#pylint: disable=E0611, E0401
class ServerHandler:
	
	def __init__(self, clientObject, mainWindow):
		
		self.guiHelper = GUIHelper(mainWindow.output)

		self.clientObject = clientObject

		self.easyRequestIds = ["001", "023", "401", "411", "031", "411", "711"]

		self.channelTreeList = list()

		self.kicked = False
		self.banned = False
		self.serverOffline = False

		while True:
			try:
				request = str(self.clientObject.socketObject.recv(1024), "utf-8")
				self.handleRequest(request, mainWindow)
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

	def handleRequest(self, request, mainWindow):
		requestId = request[:3]
		requestdata = request[3:]
		if requestId in self.easyRequestIds:
			self.guiHelper.printOutput(requestdata)
		elif requestId == "402":
			print("[Client/Info] You got kicked by the console.")
			self.kicked = True
		elif requestId == "403":
			print("[Client/Info]Server shut down.")
			self.serverOffline = True
		elif requestId == "022":
			count = 0
			countAtt = 0
			channelNames = list()
			channelDescriptions = list()
			channelPasswords = list()
			channelAccessLevels = list()
			channelAttributes = requestdata.split(":")
			self.guiHelper.printOutput("[Client/Info] Channels: ")
			for attributeList in channelAttributes:
				attributes = attributeList.split(",")
				for attribute in attributes:
					attribute = attribute.replace("'"," ").strip("[]").strip()
					if countAtt == 0:
						channelNames.append(attribute)
					elif countAtt == 1:
						channelDescriptions.append(attribute)
					elif countAtt == 2:
						channelPasswords.append(attribute)
					else:
						channelAccessLevels.append(attribute)
				countAtt = countAtt + 1
			for name in channelNames:
				self.guiHelper.printOutput(name + " desc: " + channelDescriptions[count] + " pw: " + channelPasswords[count] + " accessLevel: " + channelAccessLevels[count])
				count = count + 1
		elif requestId == "611":
			print("deleted")
		elif requestId == "405":
			self.guiHelper.printOutput(requestdata)
			self.banned = True
		elif requestId == "811":
			self.clientObject.socketObject.sendall(DecodingEncodingHelper().stringToBytes("901"))
		elif requestId == "903":
			mainWindow.statusButton.setText("Online Connected as: " + self.clientObject.username)
			self.clientObject.socketObject.sendall(DecodingEncodingHelper().stringToBytes("901"))
		elif requestId == "901":
			count = 0
			mainWindow.channelTree.clear()
			requestdata = requestdata.strip("[]")
			requestdata = requestdata.split(";")
			for channel in requestdata:
				if count == 0:
					channel = channel.strip('"')
					channel = channel.replace(" '", "")
					channel = channel.strip("'")
				else:
					channel = channel.strip('"')
					channel = channel.replace(" '", "")
					channel = channel.strip("'")
					channel = channel[1:]
					channel = channel.strip()
					channel = channel.strip('"')
				channel = channel.split(":")
				channelName = channel[0]
				member = channel[1]
				member = member.strip("[]")
				member = member.split(",")
				channelItem = QTreeWidgetItem([channelName])
				for mem in member:
					mem = mem.strip("'")
					clientItem = QTreeWidgetItem(["-" + mem])
					channelItem.addChild(clientItem)
				mainWindow.channelTree.addTopLevelItem(channelItem)
				mainWindow.channelTree.expandAll()
				count = count + 1
		
		elif requestId == "902":
			print("couldt log in")
			raise SystemExit()

		elif len(requestId) == 0:
			raise SystemExit()
		else:
			self.guiHelper.printOutput("[Client/Error] Server sent unknown requestId: " + requestId)