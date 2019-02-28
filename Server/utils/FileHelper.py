from objects.Config import Config#pylint: disable=E0611, E0401

import os, sys, json

class FileHelper:

	def writeJsonFile(self, path, fileName, dataToBeWritten):
		fileToWrite = open(path + fileName + ".json", "w")
		json.dump(dataToBeWritten, fileToWrite, indent=4)

	def createDefaultConfig(self):
		if self.generateNew:
			print("[Client/Error] Removin old one and generating the default one.")	
			os.remove("config/config.json")
			config = {
  					"Server Config": [
    					{"ip": "localhost"},
							{"port": 5000}
						],
			#		"Other Config": [
			#			{"None": "None"}
			#		]
					}
		else:
			config = {
  					"Server Config": [
    					{"ip": "localhost"},
							{"port": 5000}
						],
			#		"Other Config": [
			#			{"None": "None"}
			#		]
					}
		self.writeJsonFile("config/", "config", config)

	def createDefaultPaths(self):
		if not os.path.exists("config/"):
			os.makedirs("config/")
		if not os.path.exists("data/"):
			os.makedirs("data/")

	def createDefaultFiles(self):
		self.createDefaultConfig()
		if not os.path.isfile("data/banList.txt"):
			self.appendToTXTFile("data/" , "banList", "BanList:")
		
	def __init__(self):
		#default booleam
		self.generateNew = False
		#create default paths
		self.createDefaultPaths()
		#create default files
		self.createDefaultFiles()
			
	def readTXTFile(self, path, fileName):
		fileToRead = open(path + fileName + ".txt", "r")
		return fileToRead.readlines()

	def appendToTXTFile(self, path, fileName, textToAppend):
		fileToWrite = open(path + fileName + ".txt","a")
		fileToWrite.write(textToAppend + "\n")
		fileToWrite.close()

	def addClientToBanList(self, client):
		self.appendToTXTFile("data/" , "banList", client)

	def removeClientFromBanList(self, client):
		clientList = self.readTXTFile("data/", "banList")
		fileToWrite = open("data/banList.txt", "w")
		for clientInList in clientList:
			s = clientInList.split(":")
			if s[0] != client:
				  fileToWrite.write(clientInList)
		fileToWrite.close()		

	def readJsonFile(self, path, fileName):
		fileToRead = open(path + fileName + ".json", "r")
		try:
			return json.load(fileToRead)
		except json.decoder.JSONDecodeError:
			print("[Client/Error] Config file couldn't be read.")
			self.generateNew = True
			self.createDefaultConfig()

	def getConfig(self):
		try:
			config = self.readJsonFile("config/", "config")
			serverConfig = config["Server Config"]
			return Config(serverConfig[0]["ip"], serverConfig[1]["port"])
		except TypeError:
			print("[Client/Error] Please restart the server.")	
			raise SystemExit()