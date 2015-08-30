
class WebServer:
	
	_json = {}
	_url = None
	__device_code = 1

	def __init__(self):
		self=self

	def addRecordList(self,value):
		raise Exception

	def emptyRecordList(self):
		raise Exception

	def _updateJSON(self):
		raise Exception

	def push(self):
		raise Exception
	
	def getDeviceCode(self):
		return self.__device_code
