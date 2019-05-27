import os, datetime
class LogHelper:
	def printAndWriteServerLog(self, logType, log):
		if not os.path.exists("logs/"):
				os.makedirs("logs/")
		if logType.lower() in ("info", "error"):
			log = "[" + datetime.datetime.now().strftime("%H:%M:%S") + " " + logType.upper() + "]: " + log
			logFile = open("logs/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt","a") 
			logFile.write(log + "\n")
			logFile.close() 
		else:
			log = "[" + datetime.datetime.now().strftime("%H:%M:%S") + " Error]: Log was not written logtype is unrecognized."
		print(log)
	def printAndWriteChannelLog(self, logType, channel, log):
		if not os.path.exists("logs/channels/" + channel):
				os.makedirs("logs/channels/" + channel)
		if logType.lower() in ("info", "error"):
			log = "[" + datetime.datetime.now().strftime("%H:%M:%S") + " " + logType.upper() + " (" + channel + ") ]: " + log
			logFile = open("logs/channels/" + channel + "/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt","a")
			logFile.write(log + "\n")
			logFile.close()
		else:
			log = "[" + datetime.datetime.now().strftime("%H:%M:%S") + " Error]: Log was not written logtype is unrecognized."
		print(log)