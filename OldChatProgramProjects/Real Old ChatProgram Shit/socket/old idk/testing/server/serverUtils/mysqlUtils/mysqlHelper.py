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
		try:
			cnx = mysql.connector.connect(user = 'python_admin',
									  password = '8t7uzer49:Python',
									  #schule: 172.16.5.31
									  #zuhause jan: 192.168.2.107
									  #zuhause papa: 192.168.0.108
									  host = '192.168.2.107',
									database = 'python');
			return cnx
		except:
			print("Mysql server not Online  : SEND A PACKET TO CLIENT")
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

	def getBannedClients(self):
		result = mysqlStatement("SELECT ip, banned FROM users", self._server).execute().fetchall().close().result
		banned_users = dict()
		banned = None
		for row in result:
			for column in row:
				if banned is None:
					banned = column
				else:
					banned_users[banned] = column
					banned = None
		return banned_users

	def checkLogin(self, useroremail, password):
		return len(mysqlStatement("SELECT * FROM users WHERE (username = '" + useroremail + "' OR email = '" + useroremail + "') AND password = '" + password + "'", self._server).execute().fetchall().close().result) > 0

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

	def ban(self, ip):
		result = mysqlStatement("SELECT banned FROM users WHERE ip = '" + ip.strip() + "'", self._server).execute().fetchall().close().result
		if len(result) >= 1 and len(result[0]) >= 1 and result[0][0] == 0:
			mysqlStatement("UPDATE users SET banned = '1' WHERE ip = '" + ip.strip() + "'", self._server).escape().execute().commit().close()

	def pardon(self, ip):
		result = mysqlStatement("SELECT banned FROM users WHERE ip = '" + ip.strip() + "'", self._server).execute().fetchall().close().result
		if len(result) >= 1 and len(result[0]) >= 1 and result[0][0] == 1:
			mysqlStatement("UPDATE users SET banned = '0' WHERE ip = '" + ip.strip() + "'", self._server).escape().execute().commit().close()
			return True
		else:
			return False

	def updateAddress(self, username, address):
		mysqlStatement("UPDATE users SET ip = '" + address + "' WHERE username = '" + username + "'", self._server).escape().execute().commit().close()

	def isBanned(self, ip):
		try:
			return mysqlStatement("SELECT banned FROM users WHERE ip = '" + ip + "' ORDER BY banned DESC", self._server).execute().fetchall().close().result[0][0] == 1
		except:
			var = None