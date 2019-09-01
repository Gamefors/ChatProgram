from objects.ServerConfig import ServerConfig
from objects.MysqlServerConfig import MysqlServerConfig

import os, sys, json

class FileHelper:

	def appendToTXTFile(self, fileName, data):
		fileToWrite = open("data/" + fileName + ".txt","a")
		fileToWrite.write(data + "\n")
		fileToWrite.close()

	def readTXTFile(self, path, fileName):
		fileToRead = open(path + fileName + ".txt", "r")
		return fileToRead.readlines()

	def __init__(self):
		if not os.path.exists("data/"):
			os.makedirs("data/")
		if not os.path.isfile("config/config.json"):
			self.createDefaultConfig()
		if not os.path.isfile("data/banList.txt"):
			self.appendToTXTFile("banList", "BanList:")
		if not os.path.isfile("data/rankList.txt"):
			self.appendToTXTFile("rankList", "RankList:")

#region Config
	def createDefaultConfig(self):
		if not os.path.exists("config/"):
			os.makedirs("config/")
		print("[INFO] Config.json was regenerated.")
		config = {
  				"Server Config": [
    				{"ip": "localhost"},
					{"port": 5000}
					],
				"Mysql Server Config": [
					{"ip": "localhost"},
					{"username": "username"},
					{"password": "password"},
					{"database": "database"}
					],
				"Version": [
					{"version": "1.0.0"},
					]
				}
		configFile = open("config/config.json", "w")
		json.dump(config, configFile, indent=4)
		configFile.close()
	def getConfig(self, type):#TODO:except more specific so you can give better feedback on whats wrong with json file | at line 56
		fileToRead = open("config/config.json", "r")
		try:
			config = json.load(fileToRead)
		except json.decoder.JSONDecodeError:
			print("[ERROR] Config file couldn't be read.")
			self.createDefaultConfig()
		fileToRead.close()
		try:
			config = config[type]
		except:
			print("[INFO] Please restart the server.")	
			raise SystemExit()
		if type == "Version":
			return config[0]["version"]
		elif type == "Server Config":
			return ServerConfig(config[0]["ip"], config[1]["port"])
		elif type == "Mysql Server Config":
			return MysqlServerConfig(config[0]["ip"], config[1]["username"], config[2]["password"], config[3]["database"])
		else:
			print("[ERROR] Type is unrecognized config couldn't be loaded.")
#endregion

#region BanList
	def addClientToBanList(self, client):
		self.appendToTXTFile("banList", client)
	def removeClientFromBanList(self, client):
		fileToRead = open("data/banList.txt", "r")
		clientList = fileToRead.readline()
		fileToRead.close()
		fileToWrite = open("data/banList.txt", "w")
		for clientInList in clientList:
			s = clientInList.split(":")
			if s[0] != client:
				  fileToWrite.write(clientInList)
		fileToWrite.close()
#endregion