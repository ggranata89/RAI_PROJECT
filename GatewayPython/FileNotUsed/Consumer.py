import threading

class Consumer(threading.Thread):

	__webserver = None
	__parseframe = None
	__frame = None
	__config_dict = None
	__mng_register_file = None
	__active_timer = 0

	__num_retry = None	

	def __init__(self,webserver,parseframe,frame,mng_reg_file,lock,network,network_lock,lock_file):
		super(Consumer, self).__init__()
		self.__webserver = webserver
		self.__parseframe = parseframe 
		self.__frame = frame
		self.__mng_register_file = mng_reg_file
		self.__lock = lock
		self.__mobile_network = network
		self.__network_lock = network_lock
		self.__lock_file = lock_file

	
	def __timeout__(self):
		self.__network_lock.acquire()
		self.__num_retry = 3
		self.__network_lock.release()

		print "Tentativo di connessione, rimanenti %d! " % self.__num_retry
		while(self.__num_retry > 0):
			self.__network_lock.acquire()
			self.__mobile_network.connect()
			status = self.__mobile_network.isConnected()
			self.__network_lock.release()
			if(status):
				print "Connesso"
				self.__lock.acquire() 
				self.__webserver.push()
				self.__webserver.emptyRecordList()
				self.__lock.release()

				self.__network_lock.acquire()
				self.__mobile_network.disconnect()
				self.__network_lock.release()

			else:
				self.__network_lock.acquire()
				self.__num_retry = self.__num_retry - 1
				self.__network_lock.release()
				print "Tentativo di connessione fallito! Rimanenti %d " % self.__num_retry
				if(self.__num_retry == 0):
					self.__lock.acquire()
					self.__webserver.emptyRecordList()
					self.__lock.release()
		self.__lock.acquire()
		self.__active_timer = 0	
		self.__lock.release()
			
			
	

	def run(self):
		
		
	#	self.__lock_file.acquire()
	#	self.__mng_register_file.openFile("register.json")
	#	periodic_tx = self.__mng_register_file.getRegister("PeriodicTx")
	#	self.__mng_register_file.closeFile()	
	#	self.__lock_file.release()


	#	if(periodic_tx < 5 and self.__active_timer == 0):
			
	#		self.__network_lock.acquire()
	#		status = self.__mobile_network.isConnected()
	#		self.__network_lock.release()
		
		json = self.__parseframe.parseFrame(self.__frame)		
		self.__lock.acquire()	
		self.__webserver.addRecordList(json)
		self.__lock.release()
		print json

		#	if(status):
		#		self.__lock.acquire()
		#		self.__webserver.push()	
		#		self.__webserver.emptyRecordList()
		#		self.__lock.release()
		
	
	#	else:
	#		self.__lock.acquire()	
	#		
	#		if(self.__webserver.getRecordListLength() == 0):
	#			print json
	#			self.__webserver.addRecordList(json)
	#			t=threading.Timer(periodic_tx,self.__timeout__)
	#			t.start()
	#			self.__active_timer = 1
	#			self.__lock.release()	
	#			t.join()
	#			
	#		else:
	#			print json
	#			self.__webserver.addRecordList(json)
	#			self.__lock.release()
			
				
				
				
		
