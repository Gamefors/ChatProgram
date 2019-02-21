import mysql.connector
import time
from serverUtils.mysqlUtils.mysqlStatement import mysqlStatement
class mysqlHelper:	
	
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
		#try:
		cnx = mysql.connector.connect(user = 'python_admin',
								  password = '8t7uzer49:Python',
								  #schule: 172.16.5.31
								  #zuhause jan: 192.168.2.102
								  #zuhause papa: 192.168.0.108
								  host = '192.168.2.102',
								database = 'python');
		return cnx
#		except:
#			print("Mysql server not Online TODO: SEND A PACKET TO CLIENT")
			#stop everything after here
	#end of helper

	
	def getChannels(self):
		result = mysqlStatement("SELECT name, description FROM channels", self._server).execute().fetchall().close().result
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
		return len(mysqlStatement("SELECT * FROM users WHERE (username = '" + useroremail + "' OR email = '" + useroremail + "') AND password = '" + password + "'", self._server).execute().fetchall().close().result) > 0



##########################################################################################
##########################################################################################
##########################################################################################
	def checkRegister(self, username):
		if len(mysqlStatement("SELECT * FROM users WHERE username = '" + username + "'", self._server).execute().fetchall().close().result) > 0:
			print("true")
		else:
			print("false")
		return True
		#when registering here it should be checked if the users already exists
##########################################################################################
##########################################################################################
##########################################################################################



	def register(self, username, password, email):
		if len(mysqlStatement("SELECT * FROM users WHERE (username = '" + username + "' OR email = '" + email + "')", self._server).execute().fetchall().close().result) > 0:
			return False
		else:
			mysqlStatement("INSERT INTO users (username, password, email) VALUES ('" + username + "', '" + password + "', '" + email + "')", self._server).escape().execute().commit().close()
			return True

	def createChannel(self, channelName, channelDescription, channnelPassword, channelRequired_auth_level):
		self._server.createLogsUtil.printandwriteserverlog(self._server.serverPrefix + "created new channel" + channelName)
		mysqlStatement("INSERT INTO channels (name, description, password, required_auth_level) VALUES ('" + channelName.strip() + "', '" + channelDescription.strip() + "', '" + channnelPassword.strip() + "', '" + channelRequired_auth_level.strip() + "')", self._server).escape().execute().commit().close()
		return True

	def deleteChannel(self, channelName):
		if len(mysqlStatement("SELECT * FROM channels WHERE name = '" + channelName.strip()  + "'", self._server).execute().fetchall().close().result) > 0:
			mysqlStatement("DELETE FROM channels WHERE name = '" + channelName.strip()  + "'", self._server).escape().execute().commit().close()
			self._server.createLogsUtil.printandwriteserverlog(self._server.serverPrefix + "deleted channel" + channelName)
			return True
		else:
			return False

	def editChannel(self, channelName, toEdit, argument):
		if len(mysqlStatement("SELECT * FROM channels WHERE name = '" + channelName.strip() + "'", self._server).execute().fetchall().close().result) > 0:
			mysqlStatement("UPDATE channels SET " + toEdit.strip() + " = '" + argument.strip() + "' WHERE name = '" + channelName.strip() + "'", self._server).escape().execute().commit().close()
			self._server.createLogsUtil.printandwriteserverlog(self._server.serverPrefix + "edited channel" + channelName)
			return True
		else:
			return False

	def changeAuth_level(self, username, auth_level):
		if len(mysqlStatement("SELECT * FROM users WHERE username = '" + username.strip() + "'", self._server).execute().fetchall().close().result) > 0:
			mysqlStatement("UPDATE users SET auth_level = '" + auth_level.strip() + "' WHERE username = '" + username.strip() + "'", self._server).escape().execute().commit().close()
			self._server.createLogsUtil.printandwriteserverlog(self._server.serverPrefix + "changed Auth_level of " + username + " to " + auth_level)
			return True
		else:
			return False

	def updateIp(self, username, address):
		mysqlStatement("UPDATE users SET ip = '" + address + "' WHERE username = '" + username + "'", self._server).escape().execute().commit().close()

