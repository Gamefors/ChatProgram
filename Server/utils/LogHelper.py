import os, datetime

class LogHelper:

	def __init__(self):
		#create default paths
		self.createDefaultPaths()

	def createDefaultPaths(self):
		if not os.path.exists("logs/channels/"):
			os.makedirs("logs/channels/")

	def printAndWriteServerLog(self, msg):
		print(msg)
		self.writeServerLog(msg)
		
	def printAndWriteChannelLog(self, channel, msg):
		print(msg)
		self.writeChannelLog(channel ,msg)

	def writeServerLog(self, log):
		logFile = open("logs/" + datetime.datetime.now().strftime("%Y-%m-%d")  + ".txt","a") 
		logFile.write("[" + datetime.datetime.now().strftime("%H:%M:%S") + "]" + ":" + log + "\n")
		logFile.close() 
		
	def writeChannelLog(self, channel, msg):
			if not os.path.exists("logs/channels/" + channel):
				os.makedirs("logs/channels/" + channel)
			logFile = open("logs/channels/" + channel + "/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt","a")
			logToWrite = "[" + datetime.datetime.now().strftime("%H:%M:%S") + "]" + ":" + msg + "\n"
			logFile.write(logToWrite)
			logFile.close()