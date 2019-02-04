import mysql.connector
import time
from utils.mysqlstatement import mysqlstatement
class mysqlhelper:	
	
	#global declarations of class mysqlhelper
	#server instance
	_server = None
	#global declarations of class mysqlhelper
	
	#constructor for class mysqlhelper
	def __init__(self, server_):
		self._server = server_
	#end of constructor for class mysqlhelper

	#helper
	def openmysqlcnx(self):
		cnx = mysql.connector.connect(user = 'python_admin',
								  password = '8t7uzer49:Python',
								  host = '192.168.0.100',
								database = 'python')
		cur = cnx.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS users (id INT NOT NULL AUTO_INCREMENT, username TEXT NOT NULL,password TEXT NOT NULL,email TEXT NOT NULL,PRIMARY KEY (id))")
		cnx.commit()
		cur.execute("CREATE TABLE IF NOT EXISTS channels (id INT NOT NULL AUTO_INCREMENT, name TEXT NOT NULL, description TEXT NOT NULL, password TEXT NOT NULL, required_auth_level INT NOT NULL, PRIMARY KEY (id))")
		cnx.commit()
		return cnx
	#end of helper

	
	def getChannels(self):
		result = mysqlstatement("SELECT name, description FROM channels", self._server).execute().fetchall().close().result

		channels = dict()

		currentChannel = None

		for row in result:
			for column in row:
				if currentChannel is None:
					currentChannel = column
				else:
					channels[currentChannel] = column
					currentChannel = None

		return channels

	def checkLogin(self, useroremail, password):
		self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + useroremail + " tried to login")
		return len(mysqlstatement("SELECT * FROM users WHERE (username = '" + useroremail + "' OR email = '" + useroremail + "') AND password = '" + password + "'", self._server).execute().fetchall().close().result) > 0

	def register(self, username, password, email):
		if len(mysqlstatement("SELECT * FROM users WHERE (username = '" + username + "' OR email = '" + email + "')", self._server).execute().fetchall().close().result) > 0:
			return False
		else:
			mysqlstatement("INSERT INTO users (username, password, email) VALUES ('" + username + "', '" + password + "', '" + email + "')", self._server).escape().execute().commit().close()
			self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + "registered user " + username)
			return True

	def createChannel(self, channelName, channelDescription, channnelPassword, channelRequired_auth_level):
		self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + "created new channel" + channelName)
		mysqlstatement("INSERT INTO channels (name, description, password, required_auth_level) VALUES ('" + channelName.strip() + "', '" + channelDescription.strip() + "', '" + channnelPassword.strip() + "', '" + channelRequired_auth_level.strip() + "')", self._server).escape().execute().commit().close()
		return True

	def deleteChannel(self, channelName):
		if len(mysqlstatement("SELECT * FROM channels WHERE name = '" + channelName.strip()  + "'", self._server).execute().fetchall().close().result) > 0:
			mysqlstatement("DELETE FROM channels WHERE name = '" + channelName.strip()  + "'", self._server).escape().execute().commit().close()
			self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + "deleted channel" + channelName)
			return True
		else:
			return False

	def editChannel(self, channelName, toEdit, argument):
		if len(mysqlstatement("SELECT * FROM channels WHERE name = '" + channelName.strip() + "'", self._server).execute().fetchall().close().result) > 0:
			mysqlstatement("UPDATE channels SET " + toEdit.strip() + " = '" + argument.strip() + "' WHERE name = '" + channelName.strip() + "'", self._server).escape().execute().commit().close()
			self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + "edited channel" + channelName)
			return True
		else:
			return False

	def changeAuth_level(self, username, auth_level):
		if len(mysqlstatement("SELECT * FROM users WHERE username = '" + username.strip() + "'", self._server).execute().fetchall().close().result) > 0:
			mysqlstatement("UPDATE users SET auth_level = '" + auth_level.strip() + "' WHERE username = '" + username.strip() + "'", self._server).escape().execute().commit().close()
			self._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + "changed Auth_level of " + username + " to " + auth_level)
			return True
		else:
			return False
		
	


