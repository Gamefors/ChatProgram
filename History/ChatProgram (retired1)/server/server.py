import socket
import threading
import time
from utils.createlog import createlog
from utils.connectionuser import connectionuser
from utils.mysqlhelper import mysqlhelper
from utils.requests import requests
from utils.commands import commands
class server:

	#global declarations of class server
	#server connection
	_server = None
	#users that are connected to the server
	users = list()
	#users/connections that are being kept alive via keeping alive packages
	keptAliveConnections = dict()
	#utilities
	createlogUtil = None 
	mysqlHelperUtil = None
	requestsUtil = None
	commandsUtil = None
	#prefixes
	serverprefix = "[Server] "
	clientprefix = "[Client] "
	#end of global declarations of class server
	
	#constructor of class server
	def __init__(self):		
		self.mysqlHelperUtil = mysqlhelper(self)
		self.createlogUtil = createlog()
		self.requestsUtil = requests()
		self.commandsUtil = commands(self)

		self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self._server.bind(("192.168.0.105", 5000))
		print("Server started on" + str(self._server))

		threading.Thread(target=self.catchConnections,args=[]).start()
		threading.Thread(target=self.interpreterInput,args=[]).start()
		threading.Thread(target=self.keepAliveConnection,args=[]).start()
	#end of constructor of class server

	#helper 

	def getCurrentChannelClients(self, currentChannel):
		#get the clients from the currentChannel
		clientsInChannel = list()
		for user in self.users:
			if user.channel == currentChannel:
				clientsInChannel.append(user.username)
		return clientsInChannel
	#end of helper 

	def catchConnections(self):
		while True:
			print("Listening for clients...")
			self._server.listen(5)
			accepted = self._server.accept()
			self.createlogUtil.printandwriteserverlog(self.serverprefix + "got connection from " + str(accepted[1]) + " and started sending keep alive packages to him")
			self.users.append(connectionuser(accepted[0], accepted[1], self, self.requestsUtil))

	def interpreterInput(self):
		while True:
			command = input()
			
			if command.startswith("/"):
				commandName = command.split(" ")[0].replace("/", "") if " " in command else command.replace("/", "")

				if commandName in self.commandsUtil.availableCommands:
					args = list()
					if " " in command:
						for arg in command.split(" "):
							if not arg.startswith("/"):
								args.append(arg)

					if self.commandsUtil.availableCommands[commandName].correctArgs(args):
						self.commandsUtil.availableCommands[commandName].execute(args)
					else:
						print("Please use the following syntax: " + self.commandsUtil.availableCommands[commandName].syntax)
				else:
					self.commandsUtil.availableCommands["help"].execute([])
			else:
				self.commandsUtil.availableCommands["help"].execute([])

	def deleteConnection(self, user):				
		self.users.remove(user)
		del self.keptAliveConnections[user.address]
		self.createlogUtil.printandwriteserverlog("No keep alive packet recieved from " + (user.address[0] + ":" + str(user.address[1])) + ". Closed connection!")

	def keepAliveConnection(self):
		while True:
			time.sleep(2)
			kill = list()
			for user in self.users:
				if user.address in self.keptAliveConnections:
					if (time.time() - int(self.keptAliveConnections[user.address])) > 15:
						kill.append(user)

			for user in kill:
				try:
					user.shutdown()
					user.close()
				except:
					print("user could not be shutdowned")					
				self.deleteConnection(user)


server()




###############################################################################################################################################################

#################
#Einrahmen Bitte#
#################

# import socket
# import threading
# from mysql_helper.helper import getrooms
# from mysql_helper.login_user import login_user
# from mysql_helper.register_user import register_new_user
# from createlog import writeserverlog
# from createlog import writeroomlog
# #try:
# def printandwriteserverlog(msg):
# 	print(msg)
# 	writeserverlog(msg)


# serverprefix = "[Server] "
# clientprefix = "[Client] "
# connections = dict()
# roomUsers = dict()

# def sendmsgtoclient(msg, ip, client, port):
# 	client.send(bytes(msg, "utf-8"))
# 	printandwriteserverlog(serverprefix + "-> " + clientprefix + str(len(bytes(msg, "utf-8"))) + " bytes to [" + ip + ":" + str(port) + "]")

# def convert(msg):
# 	return str(msg, "utf-8")

# def logroom(msg, user, conn):
# 	try:
# 		global roomUsers
# 		for key, value in connections.items():

# 			if value == conn:
# 				room = roomUsers[key]
# 				name = key
# 				writeroomlog("[" + user + "] " + msg, roomUsers[user])

# 	except Exception as e:
# 		print("ERROR FROM Server:")
# 		print(e)

# server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# ip = "0.0.0.0"
# port = 5000
# adress = (ip,port)
# server.bind(adress)

# printandwriteserverlog (serverprefix + "Started server on " + ip + ":" + str(port))

# def createThreadForConn(conn):
# 	while True:
# 		global connections
# 		client = conn[0]
# 		addr = conn[1]
# 		data = None
# 		try:
# 			data = convert(client.recv(1024))	
# 		except:
# 			printandwriteserverlog(serverprefix + "ERROR: Client " + addr[0] + ":" + str(addr[1]) + " disconnected or lost connection unexpectedly")
# 			name = None 
# 			for key, value in connections.items():
# 				if value == conn:
# 					name = key
# 			del connections[name]
# 			break
# 		if len(data) is 0:
# 			continue
		
# 		printandwriteserverlog(clientprefix + "-> " + serverprefix + str(len(bytes(data, "utf-8"))) +  " bytes from [" + addr[0] + ":" + str(addr[1]) + "]")
		
# 		global roomUsers
# 		if "/" in data:
# 			validcommands = list()
# 			listofvalidcommands = ["exit"]
# 			validcommands.extend(listofvalidcommands)
# 			command2 = data.rsplit('/', 1)[-1]
# 			if command2 in validcommands:
# 				import commands
# 				if "exit" in command2:
# 					for key, value in connections.items():
# 						if value == conn:
# 							room = roomUsers[key]
# 							name = key
# 				name = commands.exit(conn,connections, roomUsers, room)
# 				del connections[name]
# 				del roomUsers[name]

# 			else:
# 				print("Command not found!")			

# 		elif "*INFORMATIONS*" in data:		
# 			infoarr = data.split(' ')
# 			if infoarr[1] in roomUsers:
# 				printandwriteserverlog(serverprefix + str(conn[1][0]) + ":" + str(conn[1][1]) + " tried to login twice. User = " + infoarr[1])
# 				sendmsgtoclient(" *[Logout]AJFF)/FKL?fkL...:;* you are already logged in with address " + str(conn[1][0]) + ":" + str(conn[1][1]) + " logging out...", conn[1][0], conn[0], conn[1][1])
# 				del connections[addr]
# 				break
# 			roomUsers[infoarr[1]] = infoarr[2]
# 			del connections[addr]
# 			connections[infoarr[1]] = conn
# 			count = 0

# 			for user, room in roomUsers.items():
# 				if room == infoarr[2]:
# 					count = count + 1
			
# 			logroom("joined Room: " + infoarr[2],infoarr[1],conn)
# 			printandwriteserverlog(serverprefix + infoarr[1] + " joined room: " + infoarr[2])
# 			for key, value in connections.items():
# 				sendmsgtoclient(" " + infoarr[1] + " joined room",value[1][0] ,value[0], value[1][1])
# 			sendmsgtoclient(" Room Informations:" ,connections[infoarr[1]][1][0], connections[infoarr[1]][0], connections[infoarr[1]][1][1])
# 			sendmsgtoclient(" ---in room " + infoarr[2] + " there are/is currently " + str(count) + " user(s) online", connections[infoarr[1]][1][0], connections[infoarr[1]][0], connections[infoarr[1]][1][1])
# 			sendmsgtoclient(" ---room description: " + infoarr[3], connections[infoarr[1]][1][0], connections[infoarr[1]][0], connections[infoarr[1]][1][1])
# 			sendmsgtoclient(" End of Room Information" ,connections[infoarr[1]][1][0], connections[infoarr[1]][0], connections[infoarr[1]][1][1])

# #INFORMATIONS AND REQUEST
# 		elif "*INFORMATIONS:LEFT" in data:
# 			leftarr = data.split(' ')
# 			for key, value in connections.items():
# 				sendmsgtoclient(" " + leftarr[1] + " left room",value[1][0] ,value[0], value[1][1])

# 		elif "*INFORMATIONS:LOGIN*" in data:
# 			loginarr = data.split(' ')
# 			result = login_user(loginarr[1],loginarr[2],loginarr[3])
# 			sendmsgtoclient("*[Login]AJFFS=)F/=K::SD* " + str((len(result)) == 1) ,conn[1][0], conn[0], conn[1][1])
# 			printandwriteserverlog(serverprefix + "Name: " + loginarr[1] + " E-Mail: " + loginarr[3] + " tried to login from [" + conn[1][0] + ":" + str(conn[1][1]) + "] Result: " + str(len(result) == 1))

# 		elif "*INFORMATIONS:REGISTER*" in data:
# 			registerarr = data.split(' ')
# 			printandwriteserverlog(serverprefix + "new user [" + registerarr[1] + "] registered with password [" + registerarr[2] + "] and email ["+ registerarr[3] + "]")
# 			register_new_user(registerarr[1],registerarr[2],registerarr[3])

# 		elif "*REQUEST:ROOMS*" in data:
# 			for key, value in connections.items():
# 				test1 = key

# 			for user, room in roomUsers.items():
# 				test2 = user
# 			printandwriteserverlog(serverprefix + "-> " + clientprefix + "sent rooms: " + str(getrooms())  + " to " + "[" + str(value[1][0]) + ":" + str(value[1][1]) + "]")
# 			for room in getrooms():
# 				sendmsgtoclient("*[Rooms]LSGK/():S* " + str(room),value[1][0] ,value[0], value[1][1])
# #END OF INFORMATIONS AND REQUEST

# #CHATTING
# 		else:
# 			room = None
# 			name = None

# 			for key, value in connections.items():
# 				if value == conn:
# 					room = roomUsers[key]
# 					name = key
# 			for key, value in connections.items():
# 				if roomUsers[key] == room:
# 					sendmsgtoclient("[" + name + "] " + data, value[1][0], value[0], value[1][1])
# 			logroom(data, name, conn)	
# #END OF CHATTING

# def listenForConnections():
# 	while True:
# 		print("listening for connections")
# 		server.listen(5)
# 		conn = server.accept()
# 		global connections
# 		connections[conn[1]] = conn[0]
# 		printandwriteserverlog(serverprefix + "Got connection from " + conn[1][0] + ":" + str(conn[1][1]))
# 		connThread = threading.Thread(target=createThreadForConn, args=[conn])
# 		connThread.start()
		

# listeningThread = threading.Thread(target=listenForConnections, args=[])
# listeningThread.start()

# def consoleInput():
# 	global connections
# 	global roomUsers
# 	command = input()
# 	if command == "clients":
# 		for key, value in connections.items():
# 			printandwriteserverlog("User " + key + " | Addr " + value[1][0] + ":" + str(value[1][1]))
# 	elif command == "rooms":
# 		for key, value in roomUsers.items():
# 			printandwriteserverlog("User " + key + " | Room " + value)
# 	consoleInput()

# consoleInput()

# #except Exception as e:
# #	print("test")
# #	print(e)