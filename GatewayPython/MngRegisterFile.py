import json
import Queue


class MngRegisterFile:
	
	__istance = None
	__out_file = None
	__register_file = []
	__file = None
	
	
	def __init__(self,file):
		if MngRegisterFile.__istance:
			raise MngRegisterFile.istance
		MngRegisterFile.__istance = self
		self.__addRegister("PeriodicTx","permanent",None,None)
		self.__addRegister("ListenPort","permanent",None,None)
		#queue =Queue.Queue()
		#self.__addRegister("ConnectionRequest","volatile","FIFO",queue)
		_buffer = ""
		self.__addRegister("ConnectionRequest","volatile","buffer",_buffer)
	
		self.__file = file

	def __addRegister(self,name,mem,_type,value):	
		self.__register_file.append(self.__setRecordRegisterFile(name,mem,_type,value))	
		

	def __setRecordRegisterFile(self,name,mem,_type,value):
		record_register_file = {}
		record_register_file["Name"] = name
		record_register_file["Mem"] = mem
		record_register_file["Type"] = _type
		record_register_file["Value"] = value
		return record_register_file

	def getRegisterFileParam(self,name):
		for i in range(0,len(self.__register_file)):
			if(self.__register_file[i]["Name"] == name):
				return self.__register_file[i]
		return None

	def openFile(self):
		MngRegisterFile.__out_file = open(self.__file,"r+")
		
	def getRegister(self,register):
		if((self.getRegisterFileParam(register)["Mem"] == "permanent")):
			self.openFile()
			MngRegisterFile.__out_file.seek(0)
			data = json.load(MngRegisterFile.__out_file)
			for key in data:
				if (key==register):	
					return data[key]
			self.closeFile()
		else:
			if((self.getRegisterFileParam(register)["Type"] == "buffer")):
				return	self.getRegisterFileParam(register)["Value"] 
			elif((self.getRegisterFileParam(register)["Type"] == "FIFO")):
				if not  self.getRegisterFileParam(register)["Value"].empty():
					return self.getRegisterFileParam(register)["Value"]
				return None
			return None
		
	
	def setRegister(self,name,value):
		if((self.getRegisterFileParam(name)["Mem"] == "permanent")):
			self.openFile()
			MngRegisterFile.__out_file.seek(0)
			data = json.load(MngRegisterFile.__out_file)
			data[name] = value

			MngRegisterFile.__out_file.seek(0)
			MngRegisterFile.__out_file.write(json.dumps(data))
    			MngRegisterFile.__out_file.truncate()	
			self.closeFile()
		else:
			if((self.getRegisterFileParam(name)["Type"] == "buffer")):
				self.getRegisterFileParam(name)["Value"] = value
			elif((self.getRegisterFileParam(name)["Type"] == "FIFO")):
				self.getRegisterFileParam(name)["Value"].put(value)
			
				

		
	def closeFile(self):
		MngRegisterFile.__out_file.close() 

