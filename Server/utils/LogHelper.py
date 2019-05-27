import os, datetime

class LogHelper:

	def __init__(self):
		#create default paths
		self.createDefaultPaths()

	def createDefaultPaths(self):
		if not os.path.exists("logs/channels/"):
			os.makedirs("logs/channels/")

	def printAndWriteServerLog(self, logType, msg):
		currTime = datetime.datetime.now().strftime("%H:%M:%S")
		if logType.lower() == "info":
			logMsg = "[" + currTime + " " + logType.upper() + "]: " + msg
			print(logMsg)
			self.writeServerLog(logMsg)
		elif logType.lower() == "error":#
			logMsg = "[" + currTime + " " + logType.upper() + "]: " + msg
			print(logMsg)
			self.writeServerLog(logMsg)
		else:
			logMsg = "[" + currTime + " Error]: Log was not written logtype is unrecognized."
			print(logMsg)
		
	def printAndWriteChannelLog(self, logType, channel, msg):

		currTime = datetime.datetime.now().strftime("%H:%M:%S")
		if logType.lower() == "info":
			logMsg = "[" + currTime + " " + logType.upper() + " (" + channel + ") ]: " + msg
			print(logMsg)
			self.writeServerLog(logMsg)
		elif logType.lower() == "error":#
			logMsg = "[" + currTime + " " + logType.upper() + "]: " + msg
			print(logMsg)
			self.writeServerLog(logMsg)
		else:
			logMsg = "[" + currTime + " Error]: Log was not written logtype is unrecognized."
			print(logMsg)

		currTime = datetime.datetime.now().strftime("%H:%M:%S")
		currTime = "[" + currTime + "]"
		logMsg = currTime + " " + msg
		print(logMsg)
		self.writeChannelLog(channel ,logMsg)

	def writeServerLog(self, log):
		logFile = open("logs/" + datetime.datetime.now().strftime("%Y-%m-%d")  + ".txt","a") 
		logFile.write(log + "\n")
		logFile.close() 
		
	def writeChannelLog(self, channel, msg):
			if not os.path.exists("logs/channels/" + channel):
				os.makedirs("logs/channels/" + channel)
			logFile = open("logs/channels/" + channel + "/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt","a")
			logToWrite = msg + "\n"
			logFile.write(logToWrite)
			logFile.close()