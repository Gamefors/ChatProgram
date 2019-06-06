from objects.Config import Config#pylint: disable=E0611, E0401

import os, sys, json

class FileHelper:

	def createDefaultConfig(self):
		if not os.path.exists("config/"):
			os.makedirs("config/")
		print("[INFO] Config.json was regenerated.")
		config = {
  				"Server Config": [
    				{"ip": "localhost"},
						{"port": 5000}
					],
				#"Other Config": [
				#	{"None": "None"}
				#]
				}
		configFile = open("config/config.json", "w")
		json.dump(config, configFile, indent=4)
		configFile.close()

	def appendToTXTFile(self, fileName, data):
		fileToWrite = open("data/" + fileName + ".txt","a")
		fileToWrite.write(data + "\n")
		fileToWrite.close()

	def __init__(self):
		if not os.path.exists("data/"):
			os.makedirs("data/")
		if not os.path.isfile("config/config.json"):
			self.createDefaultConfig()
		if not os.path.isfile("data/banList.txt"):
			self.appendToTXTFile("banList", "BanList:")
		if not os.path.isfile("data/rankList.txt"):
			self.appendToTXTFile("rankList", "RankList:")
			
	def readTXTFile(self, path, fileName):
		fileToRead = open(path + fileName + ".txt", "r")
		return fileToRead.readlines()

	def addClientToBanList(self, client):
		self.appendToTXTFile("banList", client)

	def removeClientFromBanList(self, client):
		clientList = self.readTXTFile("data/", "banList")
		fileToWrite = open("data/banList.txt", "w")
		for clientInList in clientList:
			s = clientInList.split(":")
			if s[0] != client:
				  fileToWrite.write(clientInList)
		fileToWrite.close()		

	def getConfig(self):
		fileToRead = open("config/config.json", "r")
		try:
			config = json.load(fileToRead)
		except json.decoder.JSONDecodeError:
			print("[ERROR] Config file couldn't be read.")
			self.createDefaultConfig()
		try:
			serverConfig = config["Server Config"]
		except:
			print("[INFO] Please restart the server.")	
			raise SystemExit()
		return Config(serverConfig[0]["ip"], serverConfig[1]["port"])
		
	def setStandardRankIfNotExist(self, clientObject):
		exists = False
		clientList = self.readTXTFile("data/", "rankList")
		for clientInList in clientList:
			s = clientInList.split(":")
			if s[0] == clientObject.username:
				exists = True
				clientObject.rank = s[1].strip("\n")
		if exists == False:
			self.appendToTXTFile("rankList", clientObject.username + ":user")
			clientObject.rank = "user"
	
	def addClientRank(self, clientObject, rank):
		self.appendToTXTFile("rankList", clientObject.username + ":" + rank)
		clientObject.rank = rank.strip("\n")
	
	def removeClientRank(self, clientObject):
		clientList = self.readTXTFile("data/", "rankList")
		fileToWrite = open("data/rankList.txt", "w")
		for clientInList in clientList:
			s = clientInList.split(":")
			if s[0] != clientObject.username:
				  fileToWrite.write(clientInList)
		fileToWrite.close()
		clientObject.rank = "user"