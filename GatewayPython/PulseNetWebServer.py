from WebServer import WebServer
import json
import urllib2

class PulseNetWebServer(WebServer):
	
	__record = []
	

	def __init__(self):
		self = self
		WebServer._json["num_frame"] = len(self.__record)
		WebServer._json["frame"] = self.__record
		WebServer._url = "http://gatewayrai.altervista.org/php/push.php"


	def addRecordList(self,value):
		self.__record.append(value)
		self.__updateJSON()

	def emptyRecordList(self):
		print "Svuoto lista "
		del self.__record[:]
		self.__updateJSON()

	def __updateJSON(self):
		WebServer._json["num_frame"] = len(self.__record)
		WebServer._json["frame"] = self.__record 

	def setJSONItem(self,item,value):
		WebServer._json[item]= value

	def getRecordListLength(self):
		return len(self.__record)

	
	def push(self):
		json_data = self.__createJSONFile()
		print WebServer._url	
		req = urllib2.Request(WebServer._url, json_data, {'Content-Type': 'application/json'})
		f = urllib2.urlopen(req)
                response = f.read()
                print response
                f.close()	
		print "Push sul webserver"		
			
			
	def __createJSONFile(self):	
		return json.dumps(WebServer._json)
