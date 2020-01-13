class writeFiles:

	def __init__(self):
	var = None
	self.checkIfBanned("09811")

	def addUserToBanned(self, ip):
		fileA = open("BannedUsers.txt","a") 
		fileA.write(ip + "\n")
		fileA.close() 

	def removeUserFromBanned(self, ip):
		fileR = open("BannedUsers.txt","r+")
		lines = fileR.readlines()
		fileR.seek(0)
		for line in lines:
			if line.strip() != ip:
				fileR.write(line)
		fileR.truncate()
		fileR.close()

writeFiles()