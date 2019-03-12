import json
import time
from datetime import datetime
class requests:

	_server = None
	def __init__(self, server_):
		self._server = server_
		

	def tryLogin(self, args, _connectionuser, sign):
		for user in self._server.users:
			if user.username == args[0]:
				_connectionuser._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + "Client tried to login with an account that is already logged in")
				_connectionuser.returnResult(sign, "tryLogin", [False])
				return  None


		success = _connectionuser._server.mysqlHelperUtil.checkLogin(args[0], args[1])
		_connectionuser.returnResult(sign, "tryLogin", [success])
		if success == True:
			self._server.mysqlHelperUtil.updateAddress(args[0], _connectionuser.address[0])
			_connectionuser.username = args[0]
		else:
			_connectionuser.username = ""

	def tryRegister(self, args, _connectionuser, sign): 
		success = _connectionuser._server.mysqlHelperUtil.register(args[0], args[1], args[2])
		_connectionuser.returnResult(sign, "tryRegister", [success])
			
	def listChannels(self, args, _connectionuser, sign): 
		channels = _connectionuser._server.mysqlHelperUtil.getChannels()
		_connectionuser._server.createlogUtil.printandwriteserverlog(_connectionuser._server.serverprefix + _connectionuser.username + " requested channels")
		_connectionuser.returnResult(sign, "listChannels", [str(json.dumps(channels))])

	def logout(self, args, _connectionuser, sign): 
		for connUsers in _connectionuser._server.users:
			connUsers.sendToClient(_connectionuser.username + " left the channel")		
		_connectionuser._server.createlogUtil.writechannellog(_connectionuser.username + " left channel", _connectionuser.channel)
		_connectionuser.channel = None
		_connectionuser.returnResult(sign, "logout", [True])

	def listCurrentChannelClients(self, args, _connectionuser, sign):
		_connectionuser._server.createlogUtil.writechannellog(_connectionuser.username + " used command /listClients", _connectionuser.channel)
		currentChannelClients = _connectionuser._server.getCurrentChannelClients(args[0]) 
		_connectionuser.returnResult(sign, "listCurrentChannelClients", [currentChannelClients])

	def changeChannel(self, args, _connectionuser, sign): 
		_connectionuser.channel = args[0]
		_connectionuser._server.createlogUtil.printandwriteserverlog(self._server.serverprefix + _connectionuser.username + " changed channel to " + (args[0] if args[0] is not None else "None"))
		for connUsers in _connectionuser._server.users:
			if connUsers.channel == args[0]:
				connUsers.sendToClient(_connectionuser.username + " joined your channel")		
		if args[0] is not None:
			_connectionuser._server.createlogUtil.writechannellog(_connectionuser._server.serverprefix + _connectionuser.username + " joined channel", _connectionuser.channel)
		_connectionuser.returnResult(sign, "changeChannel", [True])

	def keepAliveConnection(self, args, _connectionuser, sign):
		_connectionuser._server.keptAliveConnections[_connectionuser.address] = int(time.time())
		_connectionuser.returnResult(sign, "keepAliveConnection", [str((datetime.now().microsecond - int(args[0])) / 1000)])