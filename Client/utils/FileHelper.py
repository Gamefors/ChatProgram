#Client
from objects.Config import Config#pylint: disable=E0611, E0401
import os, sys
class FileHelper:
	def __init__(self):
		if not os.path.exists("config/"):
			os.makedirs("config/")
		if not os.path.isfile("config/config.txt"):
			self.appendToTXTFile("config/" , "config", "Config:")
			self.appendToTXTFile("config/" , "config", "-")
			self.appendToTXTFile("config/" , "config", "ip:localhost")
			self.appendToTXTFile("config/" , "config", "port:5000")
		if os.path.isfile("config/config.txt"):
			configs = self.readTXTFile("config/", "config")
			fileToWrite = open("config/config.txt", "w")
			for config in configs:
				if config == "port:\n":
					fileToWrite.write("port:" + "5000" + "\n")
				elif config == "ip:\n":
					fileToWrite.write("ip:" + "localhost" + "\n")
				else:
					fileToWrite.write(config)									
			fileToWrite.close()		

	def readTXTFile(self, path, fileName):
		fileToRead = open(path + fileName + ".txt", "r")
		return fileToRead.readlines()

	def appendToTXTFile(self, path, fileName, textToAppend):
		fileToWrite = open(path + fileName + ".txt","a")
		fileToWrite.write(textToAppend + "\n")
		fileToWrite.close()

	def getConfig(self):
		config = open("config/config.txt", "r")
		configs = config.readlines()
		return Config(int(configs[3][5:]), str(configs[2][3:]).replace("\n",""))

FileHelper()