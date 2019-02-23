from objects.Config import Config#pylint: disable=E0611, E0401

import os, sys, json

class FileHelper:

	def writeJsonFile(self, path, fileName, dataToBeWritten):
		fileToWrite = open(path + fileName + ".json", "w")
		json.dump(dataToBeWritten, fileToWrite, indent=4)

	def createDefaultConfig(self):
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

	def createDefaultFiles(self):
		if not os.path.isfile("config/config.json"):
			self.createDefaultConfig()
		#TODO:add some layer 8 problem solvers eg removing a "(" or "["
	def __init__(self):
		#create default paths
		self.createDefaultPaths()
		#create default files
		self.createDefaultFiles()
			
	def readJsonFile(self, path, fileName):
		fileToRead = open(path + fileName + ".json", "r")
		return json.load(fileToRead)

	def getConfig(self):
		config = self.readJsonFile("config/", "config")
		serverConfig = config["Server Config"]
		return Config(serverConfig[0]["ip"], serverConfig[1]["port"])

FileHelper()