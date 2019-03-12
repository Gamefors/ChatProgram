class helper:
	def __init__(self):
		var = None

	def checkForValidEmail(self, emailtobechecked):
		validemails = list()
		emails = ["gmail.com", "hotmail.de", "web.de", "yahoo.com", "t-online.de", "gmx.net"]
		validemails.extend(emails)
		if "@" in emailtobechecked:
			if any(emailtobechecked.rsplit('@', 1)[-1] in s for s in validemails):
				return True
			else:
				return False
		else:
			return False
			
	def checkForIllegalCharachters(self, msgtocheck):
		if "ä" in msgtocheck or "ö" in msgtocheck or "Ä" in msgtocheck or "Ü" in msgtocheck or "Ö" in msgtocheck or "ü" in msgtocheck or "*" in msgtocheck or "!" in msgtocheck or "§" in msgtocheck or "$" in msgtocheck or "%" in msgtocheck or "&" in msgtocheck or "/" in msgtocheck or "(" in msgtocheck or ")" in msgtocheck or "=" in msgtocheck or "?" in msgtocheck or "´" in msgtocheck or "#" in msgtocheck or "[" in msgtocheck or "]" in msgtocheck or "_" in msgtocheck or "-" in msgtocheck or "," in msgtocheck or ":" in msgtocheck or ";" in msgtocheck or "<" in msgtocheck or ">" in msgtocheck or "{" in msgtocheck or "}" in msgtocheck or "~" in msgtocheck or "+" in msgtocheck or "^" in msgtocheck:
			return True
		else:
			return False