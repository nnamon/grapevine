#!usr/bin/python

import socket
import time
import select

class LogListener:
    
    ip = "0.0.0.0"
    port = 5001
    sock = None
    logging = True

    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)

    def listen(self):
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.sock.bind((self.ip, self.port))
        filename = str(int(time.time()))
        log_file = open(filename, 'w')
        while self.logging:
            ready = select.select([self.sock], [], [], 0.025)
            if ready[0]:
                data, addr = self.sock.recvfrom(10240)
                log_file.write("HOST (%s:%d)\n" % addr)
                log_file.write(data)
                log_file.write("\nNEWSET\n")
                log_file.flush()
            
    def stop_logging(self):
        self.logging = False

