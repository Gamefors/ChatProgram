import os
import json
class requests:
	_user = None

	def __init__(self, u):
		self._user = u

	#helper
	def clearinterpreterconsole(self):
		#os.system("cls" if os.name == "nt" else "clear")
		var = None

	def ask(self,question):
		self.clearinterpreterconsole()
		print(question)
		return input()

	def checkforvalidemail(self, emailtobechecked):
		validemails = list()
		emails = ["gmail.com", "hotmail.de", "web.de", "yahoo.com", "t-online.de", "gmx.net"]
		validemails.extend(emails)
		if "@" in emailtobechecked:

			if any(emailtobechecked.rsplit('@', 1)[-1] in s for s in validemails):
				return True
			else:
				print("You E-Mail host or ending is not valid returning back to register...")
				return False
		else:
			print("Your E-Mail is not a E-Mail returning back to register...")
			return False
			

	def checkforillegalcharachters(self, msgtocheck):
		if "ä" in msgtocheck or "ö" in msgtocheck or "Ä" in msgtocheck or "Ü" in msgtocheck or "Ö" in msgtocheck or "ü" in msgtocheck or "*" in msgtocheck or "!" in msgtocheck or "§" in msgtocheck or "$" in msgtocheck or "%" in msgtocheck or "&" in msgtocheck or "/" in msgtocheck or "(" in msgtocheck or ")" in msgtocheck or "=" in msgtocheck or "?" in msgtocheck or "´" in msgtocheck or "#" in msgtocheck or "[" in msgtocheck or "]" in msgtocheck or "_" in msgtocheck or "-" in msgtocheck or "," in msgtocheck or ":" in msgtocheck or ";" in msgtocheck or "<" in msgtocheck or ">" in msgtocheck or "{" in msgtocheck or "}" in msgtocheck or "~" in msgtocheck or "+" in msgtocheck:
			print("illegal characters detected returning back to action that you wanted to perform...")
			return True
		else:
			return False
	#end of helper

	def requestRegister(self):
		
		usernametocheck = self.ask("Please type in your Username:")
		if self.checkforillegalcharachters(usernametocheck):
			self.requestRegister()
		
		emailtocheck = self.ask("Please type in your E-Mail:")
		if self.checkforillegalcharachters(emailtocheck):
			self.requestRegister()
		else:
			if not self.checkforvalidemail(emailtocheck):
				self.requestRegister()

		
		passwordtocheck = self.ask("Please type in your Password:")
		if not self.checkforillegalcharachters(passwordtocheck):		
			if len(passwordtocheck) < 5:
				print("Your Password needs to be at least 6 charachters long returning back to register ...")
				self.requestRegister()
				
		else:
			self.requestRegister()
			
		success = self._user.executeServer("tryRegister", (usernametocheck, passwordtocheck, emailtocheck))
		if "True" in success[0]:
			print("Successfully registered.")
			self.requestAction()
		else:
			print("Your username or email is already in use.")
			self.requestRegister()

	def requestAction(self):
		action = self.ask("Please choose wether you want to Login or to Register by typing 'login' or 'register'")
		if "login" in action:
			self.requestLogin()
		elif "register" in action:
			self.requestRegister()
		else:
			print("You did not choose a valid option. Please try again")
			self.requestAction()

	def requestChangeChannel(self):
		channels = json.loads(self._user.executeServer("listChannels", ["xxx"])[0])
		
		for channel, description in channels.items():
			print(channel + ": " + description)

		print("Please select one of the listed channels above by typing it")
		selectedChannel = input()
		if selectedChannel in channels:
			self._user.channel = selectedChannel
			self._user.executeServer("changeChannel", [selectedChannel])
			self.clearinterpreterconsole()
			print("Successfully changed channel to " + selectedChannel)
			self._user.inputsUtil.waitForMessage()
		else:
			print("This is not an available channel")
			self.requestChangeChannel()

	def requestLogin(self):
		
		usernametocheck = self.ask("Please type in your Username or E-Mail:")
		if self.checkforillegalcharachters(usernametocheck):
			self.requestLogin()

		passwordtocheck = self.ask("Please type in your Password:")
		if self.checkforillegalcharachters(passwordtocheck):
			self.requestLogin()
		
		success = self._user.executeServer("tryLogin", (usernametocheck, passwordtocheck))

		if "True" in success[0]:
			self.clearinterpreterconsole()
			print("Successfully logged in.")
			print("Channels:")
			self._user.username = usernametocheck
			self.requestChangeChannel()
		else:
			print("Your username or password is not correct. or the account that you are trying to log in with is already logged in on the server")
			self.requestLogin()

	