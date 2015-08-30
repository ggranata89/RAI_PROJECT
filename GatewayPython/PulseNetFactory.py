from Factory import Factory
import PulseNetWebServer
import PulseNetParseFrame
import PulseNetUartFilter

class PulseNetFactory(Factory):

	def __init__(self):
		self = self

	def newWebServer(self):
		self._WebServer = PulseNetWebServer.PulseNetWebServer()
		return self._WebServer

	def newParseFrame(self):
		self._ParseFrame = PulseNetParseFrame.PulseNetParseFrame()
		return self._ParseFrame
	
	def newUartFilter(self):
		self._UartFilter = PulseNetUartFilter.PulseNetUartFilter()
		return self._UartFilter

