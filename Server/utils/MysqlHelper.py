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
		print(config)
		try:
			self.connection = mysql.connector.connect(user = config.username , password = config.password, host = config.ip, database = config.database)
		except:
			print("Couldn't connect to Mysql Database.")#TODO: find a way to handle with this
	
		
	
	
	def ExecuteCommand(self,command):
		return MysqlStatement(command ,self.connection).execute().escape().fetchall().result

	def ExecuteCommandWithoutFetchAndResult(self, command):
		return MysqlStatement(command ,self.connection).execute().escape().commit()

	def tryLogin(self, clientObject, password):#TODO: give better fedback for layer 8 
		result = False
		if self.checkIfAccountExists(clientObject):
			if self.checkIfAccountIsLoggedIn(clientObject) == False:
				if len(self.ExecuteCommand("SELECT * FROM accounts WHERE username = '" + clientObject.username + "' and password = '" + password + "'")) > 0:
					self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET loggedIn = 1 WHERE username = '" + clientObject.username + "'")
					result = True
		return result

	def logoutAccount(self, clientObject):
		self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET loggedIn = 0 WHERE username = '" + clientObject.username + "'")

	def checkIfAccountExists(self, clientObject):
		result = False
		if len(self.ExecuteCommand("SELECT * FROM accounts WHERE username = '" + clientObject.username + "'")) > 0:
			result = True
		return result

	def checkIfAccountIsLoggedIn(self, clientObject):
		result = False
		if self.ExecuteCommand("select loggedIn,(case when loggedIn = 0 then 'loggedOut' when loggedIn = 1 then 'loggedIn' end) as loggedIn_status FROM accounts WHERE username = '" + clientObject.username + "'")[0][1] == "loggedIn":
			result = True
		return result

	def getAccountRank(self, clientObject):
		return self.ExecuteCommand("SELECT rank FROM accounts WHERE username = '" + clientObject.username + "'")[0][0]

	def updateAccountRank(self, clientObject):
		self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET rank = '" + clientObject.rank + "' WHERE username = '" + clientObject.username + "'")
		#self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET rank = 'admin' WHERE username = 'jan'")
#	def registerNewAccount(self, username, password): #FIXME: not used yet planned to get handled by a website but might get used later when you can register by ui
#		self.ExecuteCommandWithoutFetchAndResult("INSERT INTO accounts (username, password) VALUES ('" + username + "', '" + password + "')")