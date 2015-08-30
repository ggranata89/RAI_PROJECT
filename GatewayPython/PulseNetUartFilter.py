from UartFilter import UartFilter
import string
import serial
import struct

class PulseNetUartFilter(UartFilter):
	__frame = {}	
	__SIGNAL_FRAME = 0xFF
	__ALARM_FRAME =	0xAA			
	__UART_FRAME_LENGTH_EXCEPT_PAYLOAD = 15
	__ser = None
	__control_register = None
	
	def __init__(self):
		self = self
		self.__ser = serial.Serial('/dev/ttyAMA0',9600)

	def __uartGenCrc(self,data_p,length):
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

	def isFrameReady(self):
		return self.__frame["READY"]



			
	def readUartFrame(self):
		self.__frame["READY"] = 0
		s = struct.Struct('B')

		characters = self.__ser.inWaiting()
		if (characters > 0):
			self.__frame["TIPO"] =s.unpack(self.__ser.read(1))[0]
			if (self.__frame["TIPO"] == self.__SIGNAL_FRAME or self.__frame["TIPO"] == self.__ALARM_FRAME ):
			
				self.__frame["NUMBER_0"] = s.unpack(self.__ser.read(1))[0]
				self.__frame["NUMBER_1"] = s.unpack(self.__ser.read(1))[0]
				self.__frame["NUMBER_2"] = s.unpack(self.__ser.read(1))[0]
				self.__frame["NUMBER_3"] = s.unpack(self.__ser.read(1))[0]
				self.__frame["NUMBER"] = self.__frame["NUMBER_0"] << 24 | self.__frame["NUMBER_1"] << 16 | self.__frame["NUMBER_2"] << 8 | self.__frame["NUMBER_3"]
			
		
			
				self.__frame["ID"] = s.unpack(self.__ser.read(1))[0]
	

				self.__frame["COUNTER_0"] = s.unpack(self.__ser.read(1))[0]
				self.__frame["COUNTER_1"] = s.unpack(self.__ser.read(1))[0]
				self.__frame["COUNTER_2"] = s.unpack(self.__ser.read(1))[0]
				self.__frame["COUNTER_3"] = s.unpack(self.__ser.read(1))[0]
				self.__frame["COUNTER"] = self.__frame["COUNTER_0"] << 24 | self.__frame["COUNTER_1"] << 16 | self.__frame["COUNTER_2"] << 8 | self.__frame["COUNTER_3"]
		
				self.__frame["STATE"] = s.unpack(self.__ser.read(1))[0]
		
				self.__frame["DEVICE_CODE"] = s.unpack(self.__ser.read(1))[0]
			
				if(self.__frame["TIPO"] == self.__SIGNAL_FRAME):
					self.__frame["LN"] = s.unpack(self.__ser.read(1))[0]
					self.__frame["DATA"] =self.__ser.read(self.__frame["LN"])
			
				self.__frame["CRC_1"] = s.unpack(self.__ser.read(1))[0]
				self.__frame["CRC_2"] = s.unpack(self.__ser.read(1))[0]

				self.__frame["CRC"] = self.__frame["CRC_1"] << 8 | self.__frame["CRC_2"]
		

				if(self.__frame["TIPO"] == self.__SIGNAL_FRAME):	
					stream = bytearray(self.__UART_FRAME_LENGTH_EXCEPT_PAYLOAD + self.__frame["LN"])
				else:
					stream = bytearray(self.__UART_FRAME_LENGTH_EXCEPT_PAYLOAD)
				
				stream[0] = self.__frame["TIPO"]
				stream[1] = self.__frame["NUMBER_0"]
				stream[2] = self.__frame["NUMBER_1"]
				stream[3] = self.__frame["NUMBER_2"]
				stream[4] = self.__frame["NUMBER_3"]
				stream[5] = self.__frame["ID"]
				stream[6] = self.__frame["COUNTER_0"]
				stream[7] = self.__frame["COUNTER_1"]
				stream[8] = self.__frame["COUNTER_2"]
				stream[9] = self.__frame["COUNTER_3"]
				stream[10] = self.__frame["STATE"]
				stream[11] = self.__frame["DEVICE_CODE"]
				
				if(self.__frame["TIPO"] ==self.__SIGNAL_FRAME):
					stream[12] = self.__frame["LN"]
			
					index = 13
					k = 0
					tmp = bytearray(self.__frame["DATA"])
					while(k < self.__frame["LN"]):
						stream[index] = tmp[k]
						k = k + 1
						index = index + 1
				else:
					index = 12
			
				stream[index] = self.__frame["CRC_1"]
				stream[index + 1] = self.__frame["CRC_2"]
			
				if(self.__frame["TIPO"] == self.__SIGNAL_FRAME):	
					crc_stream = self.__uartGenCrc(bytearray(stream),(self.__UART_FRAME_LENGTH_EXCEPT_PAYLOAD + self.__frame["LN"]))
				else:
					crc_stream = self.__uartGenCrc(bytearray(stream),(self.__UART_FRAME_LENGTH_EXCEPT_PAYLOAD))

				if(crc_stream==0):
					self.__frame["CRC_VALIDATE"] = 1
				else:
					self.__frame["CRC_VALIDATE"] = 0
					
		
				self.__frame["READY"] = 1
						

		self.__ser.flush()
		return self.__frame
	
	def printUartFrame(self,frame):
		print "************************************"
		print ("Tipo %d") % self.__frame["TIPO"]
		print ("Number %d ") %  self.__frame["NUMBER"]
		print ("Id %d ") %  self.__frame["ID"]
		print ("Counter %d ") %  self.__frame["COUNTER"]
		print ("State %d ") %  self.__frame["STATE"]
		print ("DEVICE_CODE %d ") %  self.__frame["DEVICE_CODE"]
		print "CRC %d " %  self.__frame["CRC"]
		print "************************************"	
	
