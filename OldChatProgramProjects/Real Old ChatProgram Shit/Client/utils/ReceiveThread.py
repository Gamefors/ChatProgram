import time, sys
class ReceiveThread:
	kicked = False
	banned = False
	serverOffline = False

	def __init__(self , client):
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


		else:
			print("[Client/Error] Unknown request type")