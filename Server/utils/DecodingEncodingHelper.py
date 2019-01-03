class DecodingEncodingHelper:
	
	def bytesToString(self, bytes):
		return str(bytes, "utf-8")   

	def stringToBytes(self, string):
		return bytes(string, "utf-8")