class GUIHelper:
	
	def __init__(self, output):
		self.output = output

	def printOutput(self, msg):
		print(msg)
		self.output.append(msg)