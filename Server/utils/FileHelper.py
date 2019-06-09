from objects.ServerConfig import ServerConfig#pylint: disable=E0611, E0401
from objects.MysqlServerConfig import MysqlServerConfig#pylint: disable=E0611, E0401

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

	def getServerConfig(self):
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
		return ServerConfig(serverConfig[0]["ip"], serverConfig[1]["port"])

	def getMysqlServerConfig(self):
		fileToRead = open("config/config.json", "r")
		try:
			config = json.load(fileToRead)
		except json.decoder.JSONDecodeError:
			print("[ERROR] Config file couldn't be read.")
			self.createDefaultConfig()
		try:
			mysqlServerConfig = config["Mysql Server Config"]
		except:
			print("[INFO] Please restart the server.")	
			raise SystemExit()
		return MysqlServerConfig(mysqlServerConfig[0]["ip"], mysqlServerConfig[1]["username"], mysqlServerConfig[2]["password"], mysqlServerConfig[3]["database"])

	def getVersion(self):
		fileToRead = open("config/config.json", "r")
		try:
			config = json.load(fileToRead)
		except json.decoder.JSONDecodeError:
			print("[ERROR] Config file couldn't be read.")
			self.createDefaultConfig()
		try:
			version = config["Version"]
		except:
			print("[INFO] Please restart the server.")	
			raise SystemExit()
		return version[0]["version"]
		
	def setStandardRankIfNotExist(self, clientObject):#FIXME: will get deprecated due to mysql implementation
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
	
	def addClientRank(self, clientObject, rank):#FIXME: will get deprecated due to mysql implementation
		self.appendToTXTFile("rankList", clientObject.username + ":" + rank)
		clientObject.rank = rank.strip("\n")
	
	def removeClientRank(self, clientObject):#FIXME: will get deprecated due to mysql implementation
		clientList = self.readTXTFile("data/", "rankList")
		fileToWrite = open("data/rankList.txt", "w")
		for clientInList in clientList:
			s = clientInList.split(":")
			if s[0] != clientObject.username:
				  fileToWrite.write(clientInList)
		fileToWrite.close()
		clientObject.rank = "user"