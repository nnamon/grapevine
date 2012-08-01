#/usr/bin/python

import socket

class Host:
    # Instance Variables
    ip = "127.0.0.1"
    port = 10001
    state =  0 # Uninitialised

    # Constants
    UNINITIALISED = 0
    CONNECTED = 1

    def set_state(self, state):
        self.state = state


class HostsController:
    hosts = [] # A list of tuples in the form (addr, port)
    log_ip = "127.0.0.1" # Externally accessible host IP address.
    log_port = 5000
    sock = None
    current_vm_ip = "127.0.0.1"
    current_vm_port = 10001
    
    def __init__(self, hosts = [], log_ip = "127.0.0.1", log_port = 5000):
        self.hosts = hosts
        self.log_ip = log_ip
        self.log_port = log_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __send_cmd(self, cmd):
        self.sock.sendto(cmd, (self.current_vm_ip, 
                                  self.current_vm_port))        

    def start(self):
        pass

    def set_current_vm(self, ip, port):
        self.current_vm_ip = ip
        self.current_vm_port = int(port)

    def set_log(self, ip, port):
        self.log_ip = ip
        self.log_port = int(port)
        # Inform all hosts.

    def fuzz(self):
        self.__send_cmd("fuzz")

    def stopfuzz(self):
        self.__send_cmd("stopfuzz")

    def loadgen(self):
        self.__send_cmd("loadgen")

    def shutdownvm(self):
        self.__send_cmd("exit")
                
