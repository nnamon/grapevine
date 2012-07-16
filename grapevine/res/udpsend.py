import socket
import sys

udp_ip="127.0.0.1"
udp_port=5000

def prompt():
    sys.stdout.write( "command> ")
    uin = raw_input()
    return uin
    
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
while True:
	msg = prompt()
	sock.sendto( msg, (udp_ip, udp_port) )
	print "i've sent"