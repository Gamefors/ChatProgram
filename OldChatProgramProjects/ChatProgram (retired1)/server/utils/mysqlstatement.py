class mysqlstatement:
	
	#global declarations for class mysqlstatement
	#server instance
	_server = None
	#mysql connection and curl
	cnx = None
	cur = None
	#mysql query to execute
	stmt = None
	#mysql query result if fetched
	result = None
	#end of global declarations for class mysqlstatement
	
	#constructor for class mysqlstatement
	def __init__(self, statement, server_):
		self.stmt = statement
		self._server = server_
		self.cnx = self._server.mysqlHelperUtil.openmysqlcnx()
		self.cur = self.cnx.cursor()
	#end of constructor for class mysqlstatement

	
	def execute(self):
		self.cur.execute(self.stmt)
		return self

	def escape(self):
		self.cnx.converter.escape(self.stmt)
		return self

	def commit(self):
		self.cnx.commit()
		return self

	def fetchall(self):
		self.result = self.cur.fetchall()
		return self

	def close(self):
		self.cur.close()
		self.cnx.close()
		return self
