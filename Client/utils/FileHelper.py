from utils.GUIHelper import GUIHelper#pylint: disable=E0611, E0401

from objects.Config import Config#pylint: disable=E0611, E0401

import os, sys, json

class FileHelper:

	def createDefaultPaths(self):
		if not os.path.exists("config/"):
			os.makedirs("config/")

	def createDefaultFiles(self):
		if not os.path.isfile("config/config.json"):
			self.createDefaultConfig()
	
	def writeJsonFile(self, path, fileName, dataToBeWritten):
		fileToWrite = open(path + fileName + ".json", "w")
		json.dump(dataToBeWritten, fileToWrite, indent=4)

	def readJsonFile(self, path, fileName):
		fileToRead = open(path + fileName + ".json", "r")
		try:
			return json.load(fileToRead)
		except json.decoder.JSONDecodeError:
			self.guiHelper.printOutput("[Client/Error] Config file couldn't be read.")
			self.generateNew = True
			self.createDefaultConfig()

	def createDefaultConfig(self):
		if self.generateNew:
			self.guiHelper.printOutput("[Client/Error] Removin old one and generating the default one.")	
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


	def __init__(self):
		#imports
		self.guiHelper = GUIHelper()
		#default boolean
		self.generateNew = False
		#create default paths
		self.createDefaultPaths()
		#create default files
		self.createDefaultFiles()
			
	def getConfig(self):
		try:
			config = self.readJsonFile("config/", "config")
			serverConfig = config["Server Config"]
			return Config(serverConfig[0]["ip"], serverConfig[1]["port"])
		except TypeError:
			self.guiHelper.printOutput("[Client/Error] Please restart your client.")	
			raise SystemExit()
			