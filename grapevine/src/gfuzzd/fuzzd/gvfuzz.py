#!/usr/bin/python

import socket
import pickle

# Main entry class
class FuzzD:
    udp_ip = "127.0.0.1"
    udp_port = 10001
    logger = None
    call_mech = None
    sock = None
    generator = None

    def __init__(self, logger, call_mech, udp_ip, udp_port):
        self.logger = logger
        self.call_mech = call_mech
        self.udp_ip = udp_ip
        self.udp_port = udp_port

    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        print "Socket binding success. Listening on %d." % self.udp_port
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer 1024
            self.__handle(data, addr)

    def __handle(self, data, addr):
        """Protocol handling."""
        data = data.lower()
        if data == "loadgen":
            pass
        elif data == "dumpstate":
            pass
        elif data == "fuzz":
            log_ip = addr[0]
            log_port = int(sock.recvfrom( 512 )[0]) #recv log port
#            fuzzing = Thread(target=memfuzz,name="fuzz")
#            fuzzing.start() #starts the fuzzing function
#            checker = Timer(30.0, checkFuzz, [fuzzing]) #checks for dead fuzzing thread
#            checker.start()
        elif data == "exit":
            exit()
        else:
            self.sock.sendto("Error: Invalid command.", addr)
            




    
