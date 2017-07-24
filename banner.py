#!/usr/bin/python
# -*- coding: utf-8 -*-

# Simple Python Banner Grabber
# Created by @Viporizer

import socket
import getopt
import sys

version = "v0.4"

def head():
	print '''  ____                                  
 | __ )  __ _ _ __  _ __   ___ _ __     
 |  _ \ / _` | '_ \| '_ \ / _ \ '__|    
 | |_) | (_| | | | | | | |  __/ |       
 |____/ \__,_|_| |_|_| |_|\___|_|       
  / ___|_ __ __ _| |__ | |__   ___ _ __ 
 | |  _| '__/ _` | '_ \| '_ \ / _ \ '__|
 | |_| | | | (_| | |_) | |_) |  __/ |   
  \____|_|  \__,_|_.__/|_.__/ \___|_| '''+version+"\n"
  
def usage():
	print "Usage: banner.py -h target_host[,target_host] -p target_port[,target_port]"
	print
	print "-h --hosts                - ip address(es) to scan, comma separated"
	print "-p --ports                - port(s) to scan, comma separated"
	print "-H --host-file            - input file with hosts list"
	print "-P --port-file            - input file with ports list"
	print "-v --verbose              - Print verbose output"
	print
	print "Examples:"
	print "banner.py -h 192.168.0.1,192.168.0.2 -P /path/to/ports.txt"
	print "banner.py -H /path/to/hosts.txt -p 22,44,8080"
	#print "banner.py -H \"c:\\path\\to\\file.txt\" -p 21,35,8080"
	print "banner.py -H \"c:\\\\path\\\\to\\\\file.txt\" -p 21,35,8080"
	sys.exit(0)

def retBanner(ip, port):
	try:
		socket.setdefaulttimeout(2)
		s = socket.socket()
		s.connect((ip, port))
		banner = s.recv(1024)
		return banner
	except:
		return
		
def checkIP(lst):
	for s in lst:
		a = s.split('.')
		if len(a) != 4:
			print "[*] Too short IP address found"
			return False
		for x in a:
			if not x.isdigit():
				print "[*] Non-digit in IP address found"
				return False
			i = int(x)
			if i < 0 or i > 255:
				print "[*] Invalid IP address found"
				return False
				
def errorPort():
	print "[*] Non-digit character in ports"
	sys.exit(1)

def errorHost():
	print"[*] Error in hosts"
	sys.exit(1)

def getPorts(ports):
	portList = [int(e) if e.isdigit() else errorPort() for e in ports.split(',')]
	return portList

def getHosts(ips):
	hosts = ips.split(',')
	checkIP(hosts)
	return hosts
	
def importFile(a,item):
	try:
		portList = [line.replace(',', '\n') for line in open(a)]
		return portList
		
	except:
		print "[*] Unable to open "+item+" file"
		sys.exit(1)
	
def main():
	verbose = 0
	check = 0
	hostList = []
	portList = []
	
	if not len(sys.argv[1:]):
		head()
		usage()
	try:
		head()
		opts, args = getopt.getopt(sys.argv[1:], "p:h:P:H:v", ["Ports","Hosts","PortsFile","HostsFile","Verbose"])
			
	except getopt, GetoptError:
		print str(sys.exc_info())
		
	for o, a in opts:
		if o in ("-h", "--hosts"):
			hostList = getHosts(a)
		elif o in ("-p","--ports"):
			portList = getPorts(a)
		elif o in ("-H","--host-file"):
			hostList = importFile(a, "hosts")
		elif o in ("-P","--port-file"):
			portList = importFile(a, "ports")
		elif o in ("-v", "--verbose"):
			verbose = 1
		else:
			assert False, "Unhandled option"

	for ip in hostList:
		for port in portList:
			banner = retBanner(ip, port)
			if banner:
				check = 1
				print '[+] '+ip+':'+str(port)+' >> '+banner
			if verbose == 1 and check == 0:
				print "[*] No banner detected on "+ip+":"+str(port)
	if check == 0 and verbose == 0:
		print "[*] No banners detected"
		
if __name__ == '__main__':
	main()
