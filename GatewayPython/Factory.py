
class Factory:

	_WebServer = None
	_ParseFrame = None
	_UartFilter = None

	def __init__(self):
		self=self

	def newWebServer(self):
		raise Exception
	
	def newParseFrame(self):
		raise Exception

	def newUartFilter(self):
		raise Exception

	def getWebServer(self):
		return self._WebServer

	def getParseFrame(self):
		return self._ParseFrame

	def getUartFilter(self):
		return self._UartFilter
