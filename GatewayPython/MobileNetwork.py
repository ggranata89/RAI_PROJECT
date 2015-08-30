#!/usr/bin/python
import subprocess
import string
class MobileNetwork:
	
	__istance = None

	def __init__(self):
		if MobileNetwork.__istance:
			raise MobileNetwork.istance
		MobileNetwork.__istance = self

	def connect(self):
		p = subprocess.Popen('./sakis3g connect APN="ibox.tim.it"',shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
    			print line
	def disconnect(self):
		p = subprocess.Popen('./sakis3g disconnect APN="ibox.tim.it"',shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
    			print line

	def isConnected(self):
		p = subprocess.Popen('./sakis3g status',shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		line = p.stdout.read()
		line = string.split(line)
		if(line[0]=="Not" and line[1]=="connected."):
			return 0 
		else:
			return 1
