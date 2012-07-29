#!/usr/bin/python

import socket
import sys
from common.fuzzgenerator.gvgenerator import DefaultGenerator, RandomFI
from threading import Thread
import signal
import time

# Main entry class
class FuzzD:
    udp_ip = "0.0.0.0" #Listens on all addresses
    udp_port = 10001
    logger = None
    call_mech = None
    sock = None
    generator = None
    generator_namespace = {}
    syscall_profile = None
    fuzzing = False
    fuzz_thread = None

    def __init__(self, logger, call_mech, syscalls_profile, udp_ip="0.0.0.0", udp_port=10001):
        self.logger = logger
        self.call_mech = call_mech
        self.generator = RandomFI(syscalls_profile, 0)
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        
        # Set up the signals
        signal.signal(signal.SIGSEGV, self.__sig_handler)
        signal.signal(signal.SIGILL, self.__sig_handler)
        signal.signal(signal.SIGSYS, self.__sig_handler)
        signal.signal(signal.SIGINT, self.__interrupt_handler)

    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        print "Socket binding success. Listening on %d." % self.udp_port
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer 1024
            self.__handle(data, addr)

    def __fuzz(self):
        """Begin the fuzzing process with the specified generator inputs called by the calling mechanism."""
        while self.fuzzing:
            gin = self.generator.getNext()
            self.logger.log_syscall(gin[0], *gin[1:])
            gout = self.call_mech.call(gin[0], *gin[1:])
            self.logger.log_return(gout)
            self.generator.affectState(gout)
        

    def __sendback(self, msg, addr):
        self.sock.sendto(msg, addr)
        
    def __handle(self, data, addr):
        """Protocol handling."""
        data = data.lower().strip()
        print "Received data from host control: %s" % data
        if data == "loadgen":
            gen_name, _ = sock.recvfrom(2048)
            seed, _ = sock.recvfrom(2048)
            exe_code, _ = sock.recvfrom(1024*10)
            exec exe_code in self.generator_namespace # load dynamic code into temp namespace
            self.generator = self.generator_namespace[gen_name](self.seed, self.syscalls_profile)
            self.__sendback("generator %s loaded" % gen_name)
        elif data == "hello":
            self.__sendback("hello from %s" % self, addr)
        elif data == "dumpstate":
            self_dump = dict((name, getattr(self, name)) for name in dir(self))
            dump_to_requester = "Dump of current state:\n\n"
            dump_to_requester = dump_to_requester + "".join(("%s: %s\n" % (i, str(self_dump[i])) for i in self_dump))
            self.__sendback(dump_to_requester, addr)
        elif data == "fuzz":
            if not self.fuzzing:
                log_port = int(self.sock.recvfrom( 512 )[0]) #recv log port
                self.logger.set_logger( addr[0], log_port ) #set logger's details
                self.fuzzing = True
                self.fuzz_thread = Thread(target=self.__fuzz, name="fuzz")
                self.fuzz_thread.start()
                self.__sendback("Fuzzing is turned on.", addr)
            else:
                self.__sendback("Error: A fuzzing instance is already running.", addr)
        elif data == "stopfuzz":
            if self.fuzzing:
                self.fuzzing = False
                self.__sendback("Fuzzing is turned off.", addr)
            else:
                self.__sendback("Error: There is no fuzzing instance to stop.", addr)
        elif data == "exit":
            self.fuzzing = False
            self.__sendback("goodbye", addr)
            sys.exit()
        else:
            self.__sendback("Error: Invalid command.", addr)
            

    # Signal handling to continue fuzzing
    def __sig_handler(self, sig_no, stack_frame):
        print "Signal handled: %d." % sig_no

    def __interrupt_handler(self, sig_no, stack_frame):
        print "Interrupt signal detected, terminating program."
        self.fuzzing = False
        time.sleep(0.25)
        sys.exit()

    
    
        


    
