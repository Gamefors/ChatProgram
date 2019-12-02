from utils.FileHelper import FileHelper
from utils.LogHelper import LogHelper
import mysql.connector, datetime, sqlite3
from sqlite3 import Error
class MysqlStatement:
	
	def __init__(self, statement, connection):
		self.stmt = statement
		self.cnx = connection
		self.cur = self.cnx.cursor()

	def execute(self):
		try:
			self.cur.execute(self.stmt)
		except mysql.connector.errors.ProgrammingError as ex:
			if "Table 'chat.accounts' doesn't exist" in str(ex):
				return "createTable"
			else:
				print(ex)
				
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
		self.mysqlMode = 0 # 0 = Mysql; 1 = MysqlLite


		self.fileHelper = FileHelper()
		self.logHelper = LogHelper()
		config = self.fileHelper.getConfig("Mysql Server Config")
		try:
			self.connection = mysql.connector.connect(user = config.username , password = config.password, host = config.ip, database = config.database)
		except:
			self.mysqlMode = 1
			print("[" + datetime.datetime.now().strftime("%H:%M:%S") + " ERROR]: Couldn't establish connection to mysql database(" + config.database + ") with ip: " + config.ip)
			print("[" + datetime.datetime.now().strftime("%H:%M:%S") + " INFO]: Falling back to MysqlLite.")
			
			#sqllite

			self.conn = self.create_connection("data/database.db")
			
			checkForAccountsTable = "SELECT * FROM accounts"
			
			result = self.executeCommandOnLite(self.conn, checkForAccountsTable)
			try:
				for row in result:
					if row[0] == 1:
						result = True
					else:
						result = False
			except:
				result = False
			if result == False:
				createTableStatement = "CREATE TABLE accounts (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, rank TEXT NOT NULL, loggedIn TINYINT NOT NULL DEFAULT '0');"
				print("[" + datetime.datetime.now().strftime("%H:%M:%S") + " INFO]: Created accounts table in MysqlLite database.")
				self.executeCommandOnLite(self.conn, createTableStatement)
		
	def create_connection(self, db_file):
		try:
			conn = sqlite3.connect(db_file)
			return conn
		except Error as e:
			print(e)
			return e

	def executeCommandOnLite(self, connection, command):
		try:
			cursor = connection.cursor()
			result = cursor.execute(command)
			return result
		except Error as e:
			return e

	def ExecuteCommand(self,command):
		result = None
		try:
			result = MysqlStatement(command ,self.connection).execute().escape().fetchall().result
		except AttributeError:
			self.logHelper.log("info", "Created mysql table.")
			self.ExecuteCommandWithoutFetchAndResult("CREATE TABLE accounts ( id INT NOT NULL AUTO_INCREMENT, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, rank TEXT NOT NULL, loggedIn TINYINT NOT NULL DEFAULT '0', PRIMARY KEY (id))")

		return result

	def ExecuteCommandWithoutFetchAndResult(self, command):
		return MysqlStatement(command ,self.connection).execute().escape().commit()

	def tryLogin(self, clientObject, password):#TODO: give better fedback for layer 8
		if self.mysqlMode == 0:

			result = False
			lenght = None
			try:
				lenght = len(self.ExecuteCommand("SELECT * FROM accounts WHERE username = '" + clientObject.username + "'"))
			except:
				lenght = len(self.ExecuteCommand("SELECT * FROM accounts WHERE username = '" + clientObject.username + "'"))
			if lenght > 0:
				if self.ExecuteCommand("select loggedIn,(case when loggedIn = 0 then 'loggedOut' when loggedIn = 1 then 'loggedIn' end) as loggedIn_status FROM accounts WHERE username = '" + clientObject.username + "'")[0][1] != "loggedIn":
					if len(self.ExecuteCommand("SELECT * FROM accounts WHERE username = '" + clientObject.username + "' and password = '" + password + "'")) > 0:
						self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET loggedIn = 1 WHERE username = '" + clientObject.username + "'")
						result = True
			return result
		else:
			checkLoggedIn = "select loggedIn,(case when loggedIn = 0 then 'loggedOut' when loggedIn = 1 then 'loggedIn' end) as loggedIn_status FROM accounts WHERE username = '" + clientObject.username + "'"
			result = self.executeCommandOnLite(self.conn, checkLoggedIn)
			try:
				for row in result:
					if row[0] == 1:
						
						result = True
					else:
						result = False
			except:
				result = False
			if result == False:
				checkPW = "SELECT * FROM accounts WHERE username = '"+ clientObject.username + "' and password = '" + password + "'"
				result = self.executeCommandOnLite(self.conn, checkPW)
				try:
					for row in result:
						print(row[1])
						result = True
				except:
					result = False
				if result:
					updateStatus = "UPDATE accounts SET loggedIn = 1 WHERE username = '" + clientObject.username + "'"
					self.executeCommandOnLite(self.conn, updateStatus)
				return result

	def logoutAccount(self, clientObject):
		if self.mysqlMode  == 0:
			self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET loggedIn = 0 WHERE username = '" + clientObject.username + "'")
		else:
			logoutAccount = "UPDATE accounts SET loggedIn = 0 WHERE username = '" + clientObject.username + "'"
			self.executeCommandOnLite(self.conn, logoutAccount)

	def getAccountRank(self, clientObject):
		if self.mysqlMode  == 0:
			result = self.ExecuteCommand("SELECT rank FROM accounts WHERE username = '" + clientObject.username + "'")[0][0]
		else:
			getRank = "SELECT rank FROM accounts WHERE username = '" + clientObject.username + "'"
			result = self.executeCommandOnLite(self.conn, getRank)
			for row in result:
				print(row[0])
				result = row[0]
		return result

	def updateAccountRank(self, clientObject):
		if self.mysqlMode  == 0:
			self.ExecuteCommandWithoutFetchAndResult("UPDATE accounts SET rank = '" + clientObject.rank + "' WHERE username = '" + clientObject.username + "'")
		else:
			updateRank = "UPDATE accounts SET rank = '" + clientObject.rank + "' WHERE username = '" + clientObject.username + "'"
			self.executeCommandOnLite(self.conn, updateRank)