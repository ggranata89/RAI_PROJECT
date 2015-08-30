#!/usr/bin/env python
import socket
import sys   
import urllib2
import json

if(len(sys.argv)!=3):
	print "Run program as: python server_tcp.py <LOCAL_IP> <PORT>"
    
TCP_IP = sys.argv[1]
TCP_PORT = sys.argv[2]
my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
data = {}
data["ConnectionRequest"] = my_ip
data["CodGateway"] = 1
data["ListenPort"] = TCP_PORT
json = json.dumps(data)
print json
req = urllib2.Request( "http://gatewayrai.altervista.org/php/insConnectionRequest.php", json, {'Content-Type': 'application/json'})
f = urllib2.urlopen(req)
response = f.read()
print response
f.close()

BUFFER_SIZE = 2048  # Normally 1024, but we want fast response
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(((TCP_IP), int(TCP_PORT)))
s.listen(1)
   
conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    conn.send(data)  # echo
conn.close()
