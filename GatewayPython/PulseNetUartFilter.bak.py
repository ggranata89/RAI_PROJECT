from UartFilter import UartFilter
import string
import serial
import struct

class PulseNetUartFilter(UartFilter):

	__SIGNAL_FRAME = 0xFF
	__ALARM_FRAME =	0xAA			
	__UART_FRAME_LENGTH_EXCEPT_PAYLOAD = 15
	__ser = None
	__control_register = None
	
	def __init__(self):
		self = self
		self.__ser = serial.Serial('/dev/ttyAMA0',9600)

	def __uart_gen_crc(self,data_p,length):
		crc = 0xFFFF
		i = 0	
		x = '0'
		while(length != 0):
			length = length - 1
			x = crc >> 8 ^ data_p[i]
			i = i + 1
			x ^= x >> 4
			crc = ((crc << 8) & 0xFFFF) ^ ((x<<12) & 0xFFFF) ^ ((x <<5) & 0xFFFF) ^ (x & 0xFFFF)
		return crc	
			
	def readUartFrame(self):
		frame = {}
		frame["READY"] = 0
		s = struct.Struct('B')

		characters = self.__ser.inWaiting()
		if (characters > 0):
			frame["TIPO"] =s.unpack(self.__ser.read(1))[0]
			if (frame["TIPO"] == self.__SIGNAL_FRAME or frame["TIPO"] == self.__ALARM_FRAME ):
			
				frame["NUMBER_0"] = s.unpack(self.__ser.read(1))[0]
				frame["NUMBER_1"] = s.unpack(self.__ser.read(1))[0]
				frame["NUMBER_2"] = s.unpack(self.__ser.read(1))[0]
				frame["NUMBER_3"] = s.unpack(self.__ser.read(1))[0]
				frame["NUMBER"] = frame["NUMBER_0"] << 24 | frame["NUMBER_1"] << 16 | frame["NUMBER_2"] << 8 | frame["NUMBER_3"]
			
		
			
				frame["ID"] = s.unpack(self.__ser.read(1))[0]
	

				frame["COUNTER_0"] = s.unpack(self.__ser.read(1))[0]
				frame["COUNTER_1"] = s.unpack(self.__ser.read(1))[0]
				frame["COUNTER_2"] = s.unpack(self.__ser.read(1))[0]
				frame["COUNTER_3"] = s.unpack(self.__ser.read(1))[0]
				frame["COUNTER"] = frame["COUNTER_0"] << 24 | frame["COUNTER_1"] << 16 | frame["COUNTER_2"] << 8 | frame["COUNTER_3"]
		
				frame["STATE"] = s.unpack(self.__ser.read(1))[0]
		
				frame["DEVICE_CODE"] = s.unpack(self.__ser.read(1))[0]
			
				if(frame["TIPO"] == self.__SIGNAL_FRAME):
					frame["LN"] = s.unpack(self.__ser.read(1))[0]
					frame["DATA"] =self.__ser.read(frame["LN"])
			
				frame["CRC_1"] = s.unpack(self.__ser.read(1))[0]
				frame["CRC_2"] = s.unpack(self.__ser.read(1))[0]

				frame["CRC"] = frame["CRC_1"] << 8 | frame["CRC_2"]
		

				if(frame["TIPO"] == self.__SIGNAL_FRAME):	
					stream = bytearray(self.__UART_FRAME_LENGTH_EXCEPT_PAYLOAD + frame["LN"])
				else:
					stream = bytearray(self.__UART_FRAME_LENGTH_EXCEPT_PAYLOAD)
				
				stream[0] = frame["TIPO"]
				stream[1] = frame["NUMBER_0"]
				stream[2] = frame["NUMBER_1"]
				stream[3] = frame["NUMBER_2"]
				stream[4] = frame["NUMBER_3"]
				stream[5] = frame["ID"]
				stream[6] = frame["COUNTER_0"]
				stream[7] = frame["COUNTER_1"]
				stream[8] = frame["COUNTER_2"]
				stream[9] = frame["COUNTER_3"]
				stream[10] = frame["STATE"]
				stream[11] = frame["DEVICE_CODE"]
				
				if(frame["TIPO"] ==self.__SIGNAL_FRAME):
					stream[12] = frame["LN"]
			
					index = 13
					k = 0
					tmp = bytearray(frame["DATA"])
					while(k < frame["LN"]):
						stream[index] = tmp[k]
						k = k + 1
						index = index + 1
				else:
					index = 12
			
				stream[index] = frame["CRC_1"]
				stream[index + 1] = frame["CRC_2"]
			
				if(frame["TIPO"] == self.__SIGNAL_FRAME):	
					crc_stream = self.__uart_gen_crc(bytearray(stream),(self.__UART_FRAME_LENGTH_EXCEPT_PAYLOAD + frame["LN"]))
				else:
					crc_stream = self.__uart_gen_crc(bytearray(stream),(self.__UART_FRAME_LENGTH_EXCEPT_PAYLOAD))

				if(crc_stream==0):
					frame["CRC_VALIDATE"] = 1
				else:
					frame["CRC_VALIDATE"] = 0
					
		
				frame["READY"] = 1
						

		self.__ser.flush()
		return frame
	
	def printUartFrame(self,frame):
		print "************************************"
		print ("Tipo %d") % frame["TIPO"]
		print ("Number %d ") % frame["NUMBER"]
		print ("Id %d ") % frame["ID"]
		print ("Counter %d ") % frame["COUNTER"]
		print ("State %d ") % frame["STATE"]
		print ("DEVICE_CODE %d ") % frame["DEVICE_CODE"]
		print "CRC %d " % frame["CRC"]
		print "************************************"	
	
