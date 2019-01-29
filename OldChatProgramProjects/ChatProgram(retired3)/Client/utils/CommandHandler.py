import os
#Client
class CommandHandler:
	CommandList = dict()
	def __init__(self):
		var = None

	def handleCommand(self, command):
		if command == "/clear":
			os.system('cls' if os.name=='nt' else 'clear')
		else:
			print("[Client/WIP] Commands are not implemented yet you issued command : " + command)#FIXME:implement commands for clients e.g.:/quit or /leave or admin commands /kick /ban etc