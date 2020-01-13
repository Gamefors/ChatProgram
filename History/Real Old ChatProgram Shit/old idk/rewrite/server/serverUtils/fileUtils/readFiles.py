class readFiles:

	def __init__(self):
		var = None
		self.checkIfBanned("535325")

	def checkIfBanned(self, ip):
		fileR = open("BannedUsers.txt","r")
		lines = fileR.readlines()
		for line in lines:
			if line.strip() == ip:
				return True	
			else:
				return False		
				
readFiles()