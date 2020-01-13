import json
class packet:

	def __init__(self, packetid_, command_, data_, receiver_):
		compressed = dict()
		compressed["packetid"] = packetid_
		compressed["command"] = command_
		compressed["data"] = data_
		compressed["receiver"] = receiver_
		self.compressedPacket = bytes(json.dumps(compressed), "utf-8")