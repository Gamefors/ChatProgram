import socket
import threading
import json
import time
import struct

from clientUtils.packetsUtils.packet import packet

#packet_['packetid']
#packet_['command']
#packet_['receiver']
#packet_['data']
class client:
#global client declarations
	#prefixes
	errorPrefix = "[ERROR]: "
	#listen for inputs
	chooseAction = False
	shouldRegister = False
	shouldLogin = False
	shouldAskForChannelChange = False
	#boolean of client is timed out due to high ping
	timedOut = False
#client constructor

	def __init__(self):
		self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			self.conn.connect(("localhost", 5000))
		except:
			print(self.errorPrefix + "Server is not Online or responding")
			time.sleep(1)
			exit()
		threading.Thread(target=self.listenForInputs,args=[]).start()
		threading.Thread(target=self.listenForPackets,args=[]).start()
		self.chooseAction = True
#client helper

	def ask(self, question):
		print(question)
		return input()

	def sendPacketToServer(self, packet_):
		if not self.timedOut:
			self.conn.send(packet_.compressedPacket)
#client threads

	def listenForInputs(self):
		while not self.timedOut:
			msg = None

			if self.chooseAction:
				msg = self.ask("Please choose wether you want to 'login' or 'register'")
				if "login" in msg:
					self.shouldLogin = True
					self.chooseAction = False
				elif "register" in msg:
					self.shouldRegister = True
					self.chooseAction = False
				else:
					print("This is not a valid option. Try again.")
			elif self.shouldLogin:
				username = self.ask("Username: ")
				password = self.ask("Password: ")
				self.sendPacketToServer(packet("1", "login", [username, password], "localhost"))
				self.shouldLogin = False
			elif self.shouldRegister:
				username = self.ask("Username: ")
				password = self.ask("Password: ")
				eMail = self.ask("E-Mail:")
				self.sendPacketToServer(packet("0", "register", [username, password, eMail], "localhost"))
				self.shouldRegister = False


			elif self.shouldAskForChannelChange:
				self.sendPacketToServer(packet("2", "listChannels", ["None"], "localhost"))
				channel = self.ask("Please choose a channel")
				self.sendPacketToServer(packet("3", "changeChannel", [channel], "localhost"))
				self.shouldAskForChannelChange = False


	def listenForPackets(self):
		while not self.timedOut:		
			try:
				packet_ = str(self.conn.recv(8192), "utf-8")
			except:
				print(self.errorPrefix + "Server had an unexpected shutdown")
				self.timedOut = True
				break
			try:
				packet_ = json.loads(packet_)
			except:
				print(self.errorPrefix + "Packet is a NoneType or Dictionary")
				self.timedOut = True
				break
					
			if "0" == packet_['packetid']:
				if "False" in packet_['data']:
					print("Registration was not succesfull")
					self.chooseAction = True
				else:
					print("Registration was succesfull")
					self.chooseAction = True
			elif "1" == packet_['packetid']:
				if "False" in packet_['data']:
					print("Login was not succesfull")
					self.chooseAction = True
				else:
					print("Login was succesfull")
					self.shouldAskForChannelChange = True

			elif "2" == packet_['packetid']:
				print("Channels:")
				for channel in packet_['data']:
					for name,description in channel.items():
						print(name + " : " + description)

			elif "3" == packet_['packetid']:
				if "False" in packet_['data']:
					print("please enter a valid channel")
					self.shouldAskForChannelChange = True
				else:
					print("succesfully changed channel")
					threading.Thread(target=self.WaitForChatMessage,args=[]).start()
					#chatting begins



			elif "4" == packet_['packetid']:
				print("You got banned from the server")
				self.timedOut = True
				break
			elif "5" == packet_['packetid']:
				print("you got kicked from the channel")
				self.sendPacketToServer(packet("2", "listChannels", ["None"], "localhost"))
			elif "6" == packet_['packetid']:
				var = None
			elif "7" == packet_['packetid']:
				if "False" in packet_['data']:
					print("server closed connection due to high ping")
					self.timedOut = True
					break
				else:
					self.sendPacketToServer(packet("7", "keepAlivePackage", [time.time()], "localhost"))
			elif "8" == packet_['packetid']:
				if "True" in packet_['data']:
					print("server has shutdown")
					self.timedOut = True
					break
			elif "10" == packet_['packetid']:
				print(packet_['data'][0][0])

	def WaitForChatMessage(self):
		while not self.timedOut:
			msg = input()
			if "/" in msg:
				print("command found")
			else:
				self.sendPacketToServer(packet("10", "chatMsg", [msg], "localhost"))



#initialize server
client()