import select
class Connection:

	def __init__(self, conn, addr):
		self.connection = conn
		self.address = addr
		self.authenticated = False
		self.currentChannel = None


	def tryRecv(self):
		readyForRecv = select.select([self.connection], [], [], 2)#time the select should wait to be rady again
		if readyForRecv[0]:
			self.data = str(self.connection.recv(8192), "utf-8")
			if len(self.data) > 0:
				packetid = self.data[:3]
				msg = self.data[3:]
				chatMsg = self.handlePacket(packetid, msg)
				return chatmsg
		else:
			print("no bytes to receive")
				

	def handlePacket(self, packetid, msg):
		if packetid == "001":
			self.connection.send(bytes(packetid + "1" ,"utf8"))
		elif packetid == "002":
			self.connection.send(bytes(packetid + "channels from mysql query: channel1" ,"utf8"))
		elif packetid == "003":
			print(str(self.address) + " changed chanel from " + str(self.currentChannel) + " to " + msg)
			self.connection.send(bytes(packetid + "you changed channel from " + str(self.currentChannel) + " to " + msg ,"utf8"))	
			self.currentChannel = msg
		elif packetid == "004":
			return msg

