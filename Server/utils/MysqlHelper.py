from utils.FileHelper import FileHelper#pylint: disable=E0611,E0401

import mysql.connector

class MysqlStatement:
	
	def __init__(self, statement, connection):
		self.stmt = statement
		self.cnx = connection
		self.cur = self.cnx.cursor()

	def execute(self):
		self.cur.execute(self.stmt)
		return self

	def escape(self):
		self.cnx.converter.escape(self.stmt)
		return self

	def commit(self):
		self.cnx.commit()
		return self

	def fetchall(self):
		self.result = self.cur.fetchall()
		return self

	def close(self):
		self.cur.close()
		self.cnx.close()
		return self

class MysqlHelper:

	def __init__(self):
		self.fileHelper = FileHelper()
		config = self.fileHelper.getConfig("Mysql Server Config")
		try:
			self.connection = mysql.connector.connect(user = config.username , password = config.password, host = config.ip, database = config.database)
		except:
			print("Couldn't establish connection to mysql database(" + config.database + ") with ip: " + config.ip)#TODO: find a way to handle with this
	
	def ExecuteCommand(self,command):
		result = MysqlStatement(command ,self.connection).execute().escape().fetchall().result
		print(result)
		return result

	def ExecuteCommandWithoutFetchAndResult(self, command):
		return MysqlStatement(command ,self.connection).execute().escape().commit()

	def tryLogin(self, clientObject, password):#TODO: give better fedback for layer 8 
		result = False
		if len(self.ExecuteCommand("SELECT * FROM accounts WHERE username = '" + clientObject.username + "'")) > 0:
			if self.ExecuteCommand("select loggedIn,(case when loggedIn = 0 then 'loggedOut' when loggedIn = 1 then 'loggedIn' end) as loggedIn_status FROM accounts WHERE username = '" + clientObject.username + "'")[0][1] != "loggedIn":
				if len(self.ExecuteCommand("SELECT * FROM accounts WHERE username = '" + clientObject.username + "' and password = '" + password + "'")) > 0:
					self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET loggedIn = 1 WHERE username = '" + clientObject.username + "'")
					result = True
		return result

	def logoutAccount(self, clientObject):
		self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET loggedIn = 0 WHERE username = '" + clientObject.username + "'")

	def getAccountRank(self, clientObject):
		return self.ExecuteCommand("SELECT rank FROM accounts WHERE username = '" + clientObject.username + "'")[0][0]

	def updateAccountRank(self, clientObject):
		self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET rank = '" + clientObject.rank + "' WHERE username = '" + clientObject.username + "'")