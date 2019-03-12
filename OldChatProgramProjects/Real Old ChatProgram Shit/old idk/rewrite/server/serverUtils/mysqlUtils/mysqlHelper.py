import mysql.connector
import time
from serverUtils.mysqlUtils.mysqlStatement import mysqlStatement
class mysqlHelper:	
	
	#global declarations of class mysqlhelper
	#server instance
	_server = None
	#global declarations of class mysqlhelper
	
	#constructor for class mysqlhelper
	def __init__(self, server_):
		self._server = server_
	#end of constructor for class mysqlhelper

	#helper
	def openmysqlcnx(self):
		#try:
		cnx = mysql.connector.connect(user = 'python_admin',
								  password = '8t7uzer49:Python',						
								  host = '192.168.2.102',
								database = 'python');
		return cnx