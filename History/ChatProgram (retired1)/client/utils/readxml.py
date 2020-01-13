import xml.etree.ElementTree
class readxml:
	filename = None 
	serveraddress = None
	
	def __init__(self):
		var = None
		print("1")

	def read(self, filename):
		self.filename = filename
		file = xml.etree.ElementTree.parse(filename).getroot()

		ip = file.findall("ip")
		port = file.getElementsByTagName("port")
		
		self.serveraddress = {ip:str(port)}
		print(str(serveraddress))
		#return self.serveraddress



