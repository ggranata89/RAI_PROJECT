from ParseFrame import ParseFrame

class PulseNetParseFrame(ParseFrame):
	__SIGNAL_FRAME = 0xFF
	__ALARM_FRAME =	0xAA			
	__REGISTRATION_FRAME = 0
        __DATA_FRAME = 1
	

	def __init__(self):
		#super(PulseNetParseFrame,self).__init__()
		self = self
	
	def parseFrame(self,frame):
		if(self.__isSignalFrame(frame["TIPO"])):
			dl = self.__readDLFrame(frame)
			app = self.__readAppFrame(dl)
			json = self.__JSONifySignalFrame(frame,dl,app)
		else:
			json = self.__JSONify(frame)	
		return json
	
	def __readDLFrame(self,frame):
        	DL = {}
		data = frame["DATA"]
		tipo = frame["TIPO"]
        	frame = bytearray(data)
        	DL["CL"] = frame[0]
        	DL["ID"] = frame[1]
        	DL["BC"] = frame[2]
        	DL["ST"] = frame[3]
        	DL["LN"] = frame[4]
	        DL["PAYLOAD"] = frame[5:5+DL["LN"]]
		DL["CRC_1"] = frame[DL["LN"]+5]
        	DL["CRC_2"] = frame[DL["LN"]+6]
        	DL["CRC"] = DL["CRC_1"] << 8 | DL["CRC_2"]
        	return DL

	def __readAppFrame(self,dl):
		data = dl["PAYLOAD"]
        	Record = []
       	 	App = {}
        	App["TY"] = data[0]
        	App["RS"] = data[1]
        	App["RN"] = data[2]
        	index = 3
        	if(App["TY"] == self.__REGISTRATION_FRAME):
                	for i in range(0,App["RN"]):
                        	Unit = {}
                        	Unit["IL"] = data[index]
                        	index = index + 1
                        	t0 = data[index]
                        	index = index +1
                        	t1 = data[index]
                        	index = index +1
                        	t2 = data[index]
                        	index = index +1
                        	t3 = data[index]
                        	index = index + 1
                        	Unit["TP"] = t0 << 24 | t1 << 16 | t2 << 8 | t3
                        	Unit["TMR"] = data[index]
                        	index = index + 1
                        	Record.append(Unit)
        	else:
			print "RN is %d " % App["RN"]
                	for i in range(0,App["RN"]):
                        	Unit = {}
                        	Unit["IL"] = data[index]
                        	index = index + 1
                        	Unit["NRT"] = data[index]
                        	index = index + 1
                        	ln = ((Unit["IL"] & 0xE0) >> 5) & 0x07
                        	Unit["DATA"] = 0
                        	for i in range(0,ln):
                                	Unit["DATA"] = Unit["DATA"] | data[index] << 8*(ln - 1-i)
                                	index = index + 1                               
                        	Record.append(Unit)
        	App["RECORD"] = Record             
        	return App
	

	def __isSignalFrame(self,tipo):
		if(tipo == self.__SIGNAL_FRAME):
			return 1
		return 0

	def __isAlarmFrame(self,tipo):	
		if(tipo == self.__ALARM_FRAME):
			return 1
		return 0

	def __isRegistrationFrame(self,tipo):
		if(tipo == self.__REGISTRATION_FRAME):
			return 1
		return 0
	def __isDataFrame(self,tipo):
		if(tipo == self.__DATA_FRAME):
			return 1
		return 0

	def __JSONifySignalFrame(self,frame,dl,app):
		json = {}
		record = []
		json["TYPE"] = frame["TIPO"]
		json["ID_NODE"] = frame["ID"]
		json["STATE"] = frame["STATE"]
		json["COD_RX_DEVICE"] = frame["DEVICE_CODE"]
		json["CL"] = dl["CL"]
		json["BC"] = dl["BC"]
		json["ST"] = dl["ST"]
		json["TY"] = app["TY"]
		json["RN"] = app["RN"]	
	
		for i in range(0,app["RN"]):
			payload = {}
			payload["IL"] = app["RECORD"][i]["IL"]
			if(self.__isRegistrationFrame(app["TY"])):
				payload["TP"] = app["RECORD"][i]["TP"]
				payload["TMR"] = app["RECORD"][i]["TMR"]
			elif(self.__isDataFrame(app["TY"])):
				payload["NRT"] = app["RECORD"][i]["NRT"]
				payload["DATA"] = app["RECORD"][i]["DATA"]
			record.append(payload)
		json["payload"] = record
		
		return json

	def __JSONify(self,frame):
		json = {}
		record = []
		json["TYPE"] = frame["TIPO"]
		json["ID_NODE"] = frame["ID"]
		json["STATE"] = frame["STATE"]
		json["COD_RX_DEVICE"] = frame["DEVICE_CODE"]
		json["CL"] = 0
		json["BC"] = 0
		json["ST"] = 0
		json["TY"] = 0
		json["RN"] = 0
	
		return json

	 


