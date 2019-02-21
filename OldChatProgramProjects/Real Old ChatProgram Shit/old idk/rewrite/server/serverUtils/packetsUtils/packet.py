import json
class packet:
	
	def __init__(self, packetid_, command_, data_, receiver_):
		compressed = dict()
		compressed["packetid"] = packetid_
		compressed["command"] = command_
		compressed["data"] = data_
		compressed["receiver"] = receiver_[1][0] + ":" + str(receiver_[1][1])	
		self.receiver = receiver_[0] #only needed serversided
		self.compressedPacket = bytes(json.dumps(compressed), "utf-8")