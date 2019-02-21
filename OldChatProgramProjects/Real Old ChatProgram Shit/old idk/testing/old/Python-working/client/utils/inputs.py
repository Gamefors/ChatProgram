import threading
class inputs:

	#global declarations for inputs class
	_user = None
	#end of global declarations for inputs class

	#constructor of inputs class
	def __init__(self, u):
		self._user = u
	#end of constructor of inputs class
	
	def waitForMessage(self):
		msg = input()
		if "/" in msg:
			if "listClients" in msg:
				self._user.commandsUtil.listClients()
			elif "exit" in msg:
				self._user.commandsUtil.logout()
			
			elif "help" in msg:
				self._user.commandsUtil.help()
			else:
				print("Command " + msg.replace("/", "") + "not found please type /help for a list of command") # sepereate commands from users with permissions and withut add it to todo if not done here
				self.waitForMessage()
		
		else:
			self._user.sendData(msg)

		self.waitForMessage()