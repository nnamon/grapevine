import socket

UDP_IP="0.0.0.0" #listens on all the address the machines has, DO NOT CHANGE TO LOCALHOST
UDP_PORT=10001

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock.bind( (UDP_IP, UDP_PORT) )

print 'Start listener aka gfuzzd instance...'
while True:
    message, addr = sock.recvfrom(1024)
    print 'message (%s) from : %s' % ( str(message), addr[0] )
