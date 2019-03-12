import copy
class messaging:
	
	#global declarations for messaging class
	prefix = "[%r] [%u] "
	_user = None
	#end of global declarations for messaging class

	#constructor of messaging class
	def __init__(self, u):
		self._user = u
	#end of constructor of messagin class


	def chatmessage(self, msg):
		if (msg is None) or ("*" in msg):
			return ""
			
		print(msg)