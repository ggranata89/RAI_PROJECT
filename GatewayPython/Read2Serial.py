
#! /usr/bin/python
import serial
import string

ser = serial.Serial('/dev/ttyAMA0')
#ser.open()

def readLine(ser):
	str = ""
	while(1):
		#ser.flush()	
		ch = ser.read(1)
		if (ch == "\n" or ch == "\r" or ch == ""):
			break
		str += ch
	return str

while True:
	try:
		line = readLine(ser)
		print line
	except KeyboardInterrupt:
		ser.close()
		print "Goodbye!!!"
		raise  
