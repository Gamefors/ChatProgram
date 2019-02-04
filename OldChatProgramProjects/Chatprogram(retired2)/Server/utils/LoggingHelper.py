import os, datetime
class LoggingHelper: #written by Gamefors(aka. Jan)	
	def __init__(self):
		if not os.path.exists("logs/channels/"):
			os.makedirs("logs/channels/")
	def printAndWriteServerLog(self, msg):
		print(msg)
		self.writeServerLog(msg)	
	def printAndWriteChannelLog(self, msg):
		print(msg)
		self.writeChannelLog(msg)	
	def writeServerLog(self, log):
		logFile = open("logs/" + datetime.datetime.now().strftime("%Y-%m-%d")  + ".txt","a") 
		logFile.write("[" + datetime.datetime.now().strftime("%H:%M:%S") + "]" + ":" + log + "\n")
		logFile.close() 
	def writeChannelLog(self, log):
			logFile = open("logs/channels/" + "/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt","a")
			logToWrite = "[" + datetime.datetime.now().strftime("%H:%M:%S") + "]" + ":" + log + "\n"
			logFile.write(logToWrite)
			logFile.close()