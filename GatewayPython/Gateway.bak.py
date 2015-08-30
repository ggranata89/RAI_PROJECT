import MobileNetwork
import MngRegisterFile
#import PulseNetParseFrame
import PulseNetFactory
import PulseNetUartFilter
import Consumer
import copy
import threading
import multiprocessing
import time
import os
import json
import urllib2
import Queue
import socket
import string

global isInConnect
isInConnect = 0


def loadConfiguration(mng_reg_file):
	config_dict = {}
	#mng_reg_file.openFile("register.json")
	config_dict["PeriodicTx"] = mng_reg_file.getRegister("PeriodicTx")
	#mng_reg_file.closeFile()
	return config_dict

def now():
	return round(time.time())


def threadNetworkConnect(mobile_network, web_server,mng_reg_file,network_lock,lock,lock_file,generic_lock):
	global isInConnect
	global last_send	
	network_lock.acquire()
	#print now()
	#print "Thread ID %d ora: %d " % (threading.current_thread(),now())
	status = mobile_network.isConnected()
	#print now()
	#print "Thread ID %d ora: %d " % (threading.current_thread(),now())
	network_lock.release()

	lock_file.acquire()
	periodic_tx = mng_reg_file.getRegister("PeriodicTx")
	lock_file.release()

	
	if(status == 0):
		network_lock.acquire()
		
		if(int(periodic_tx)<5 or ((int(periodic_tx))>=5 and (abs(now() - last_send)>= int(periodic_tx))))   :	

			for i in range(0,1):
				print "Tentativo di connessione... Rimanenti %d" %(2-i)
				mobile_network.connect()
				if(mobile_network.isConnected()):
					break
				if(i==3):
					lock.acquire()
					web_server.emptyRecordList()
					lock.release()
		network_lock.release()
		
	else:
		
		if (int(periodic_tx) < 5):
			lock.acquire()
			web_server.push()
			generic_lock.acquire()
			last_send = now()
			generic_lock.release()
			web_server.emptyRecordList()	
			lock.release()
		else:
			generic_lock.acquire()
			if (abs(now() - last_send)>= int(periodic_tx)):
				lock.acquire()
				web_server.push()
				web_server.emptyRecordList()
				lock.release()	
				last_send = now()
				network_lock.acquire()
				print "Disconnessione in corso...."
				mobile_network.disconnect()
				network_lock.release()
			generic_lock.release()
	generic_lock.acquire()
	isInConnect=0
	generic_lock.release()


def threadConsumer( lock,parseframe,webserver,frame,queue_lock):
		global queue
		global num_thread
		json = parseframe.parseFrame(frame)		
		lock.acquire()
		webserver.addRecordList(json)
		lock.release()
		queue_lock.acquire()
		if (num_thread > 0 ):
			queue.put(json)	
		queue_lock.release()
		print "Timestamp attuale %d " % now()
		print json

def threadMngConnect(mobile_network, web_server,mng_reg_file,network_lock,lock,lock_file,generic_lock):
	global isInConnect
	global last_send
	generic_lock.acquire()
	#tmp=isInConnect;
	#generic_lock.release()
	#if(tmp == 0):
		
	if(isInConnect == 0):
		thread = threading.Thread(target = threadNetworkConnect, args = (mobile_network,web_server,mng_reg_file,network_lock,lock,lock_file,generic_lock))
		#generic_lock.acquire()
		isInConnect = 1
		#generic_lock.release()
		thread.start()
		#thread.join()
	generic_lock.release()
	
def  threadTaskManager(WebServer,MngRegisterFile,lock_file):
	dic = {}
	dic["code"] = WebServer.getDeviceCode() 
	while(1):
		try:
			json_data = json.dumps(dic)
			WebServer._url = "http://gatewayrai.altervista.org/php/readTask.php"	
			req = urllib2.Request(WebServer._url, json_data, {'Content-Type': 'application/json'})
			f = urllib2.urlopen(req)
                	response = f.read()
                	j = json.loads(response)
			for i in range(0,len(j["task"])):
				lock_file.acquire()
				MngRegisterFile.setRegister(j["task"][i]["register-name"],j["task"][i]["value"])
				lock_file.release()
			WebServer._url = "http://gatewayrai.altervista.org/php/deleteTask.php"	
			req = urllib2.Request(WebServer._url, json_data, {'Content-Type': 'application/json'})
			f = urllib2.urlopen(req)
                	response = f.read()
			#print response
                	f.close()	
			
			time.sleep(10)
		except urllib2.URLError:
			pass 



def threadClientConnect(ip,mng_reg_file,queue_lock,lock_file):
	global queue
	global num_thread
	lock_file.acquire()
	porta = mng_reg_file.getRegister("ListenPort")
	lock_file.release()
 	if(porta == 0 or porta > 65535):
		porta = 4000 
	print porta
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client.connect((str(ip),porta))
		print "connect"
	except Exception:
		pass	
	while(1):
		try:
			#ev_sync.wait()
			#ev_sync.clear()
			queue_lock.acquire()
			if(not queue.empty()):
				record = queue.get()
				#queue.put(record)
				print "invio dato"
				sent_byte = client.send(str(record))	
				if(sent_byte == 0):
			#		queue_lock.acquire()
			#		num_thread = num_thread -1 
			#		queue_lock.release()
					print "Connessione interotta"
					break	
				#	ev.set()
		except Exception:
			break
		finally:
			queue_lock.release()
			

		




def threadSocketManager(mng_reg_file,lock_file,queue_lock):
	global queue
	global num_thread
	ev = threading.Event()
	ev_sync = threading.Event()
	num_thread = 0

	while(1):
		lock_file.acquire()
		ip = mng_reg_file.getRegister("ConnectionRequest")
		print ip
		mng_reg_file.setRegister("ConnectionRequest","")
		lock_file.release()
		#ip = "82.53.43.122"
		if(ip != None):
			while(ip != ""):
				print "Avvio un thread per soddisfare la connessione"
				t = threading.Thread(target = threadClientConnect, args = (ip,mng_reg_file,queue_lock,lock_file))
				t.start()
				ip = ""
				num_thread =  1
				t.join()
			#	queue_lock.acquire()
				num_thread = 0
			#	queue_lock.release()
		'''
		if(not queue.empty()):
			ev_sync.set()
			for i in range(0,num_thread):
				ev.wait()
				ev.clear()
			queue_lock.acquire()
			if(num_thread > 0):
				item = queue.get()
				print "svuoto il dato"
			queue_lock.release()
		'''
		time.sleep(10)	

	
def main():
	global queue
	global last_send
	queue = Queue.Queue()
	global isInConnect
	if os.geteuid() != 0:
   		 exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
	
	config_dict = {}
	last_send = now()
	factory = PulseNetFactory.PulseNetFactory()
	uart_filter = factory.newUartFilter()
	web_server = factory.newWebServer()
	parse_frame = factory.newParseFrame()

	mng_reg_file = MngRegisterFile.MngRegisterFile("register.json")
	mobile_network = MobileNetwork.MobileNetwork()
	config_dict = loadConfiguration(mng_reg_file)
	lock = threading.Lock()
	network_lock = threading.Lock()
	lock_file = threading.Lock()
	generic_lock = threading.Lock()		
	queue_lock = threading.Lock()

	conn_request_thread = threading.Thread(target = threadTaskManager, args = (web_server,mng_reg_file,lock_file))
	conn_request_thread.start()

	socket_manager_thread = threading.Thread(target = threadSocketManager, args =(mng_reg_file,lock_file,queue_lock))
	socket_manager_thread.start()

		
	
	while(1):
		try:
			frame =uart_filter.readUartFrame()		
			if (uart_filter.isFrameReady()):
				consumer = threading.Thread(target = threadConsumer, args = (lock,parse_frame,web_server,copy.copy(frame),queue_lock))
				consumer.start()
				mng_connect = threading.Thread(target = threadMngConnect, args = (mobile_network,web_server,mng_reg_file,network_lock,lock,lock_file,generic_lock))
				mng_connect.start()
				
						
		except KeyboardInterrupt:
			os._exit(1)
main()
