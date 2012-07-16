import socket

#UDP_IP="127.0.0.1"
#UDP_PORT=5000
class listener:

    def spawn(ip, port):
        sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        sock.bind( (ip, port) )

        while True:
            data, addr = sock.recvfrom( 1024 )
            print data
