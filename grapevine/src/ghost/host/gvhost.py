#/usr/bin/python

import socket

class Host:
    """Host does monitoring of the host and allows control through callbacks."""
    # Instance Variables
    ip = "127.0.0.1"
    port = 10001
    state =  0 # Uninitialised
    sock = None
    callback_set = {}

    # Constants
    UNINITIALISED = 0
    CONNECTED = 1

    def __init__(self, ip, port, callback_set = {}):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.start()

    def __send_cmd(self, data):
        self.sock.sendto(data, (self.current_host.ip, self.current_host.port))

    def start():
        pass

    def monitor():
        pass
    
    def stop():
        pass

    def set_state(self, state):
        self.state = state
        
    def is_host(self, ip, port):
        if self.ip == ip and self.port == port:
            return True
        else:
            return False


class HostsController:
    hosts = [] # A list of Hosts
    log_ip = "127.0.0.1" # Externally accessible host IP address.
    log_port = 5000
    sock = None
    current_host = None
    
    def __init__(self, hosts = [], log_ip = "127.0.0.1", log_port = 5000):
        # hosts is to be a list of tuples in the form (addr, port)
        for i in hosts:
            ip, port = i
            self.add_new_host(ip, port)
        self.log_ip = log_ip
        self.log_port = log_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __send_cmd(self, cmd):
        self.sock.sendto(cmd, (self.current_host.ip, 
                                  self.current_host.port))        

    def connect(self, ip, port):
        new_host = True
        for i in hosts:
            if i.is_host(ip, port):
                new_host = False
        if new_host:
            self.add_new_host(ip, port)
        self.set_current_host(ip, port)

    def add_new_host(self, ip, port):
        for i in hosts:
            if i.is_host(ip, port):
                return False
        new_host = Host(ip, port)
        hosts.append(new_host)

    def remove_host(self, ip, port):
        for i in hosts:
            if i.is_host(ip, port):
                i.stop()
                hosts.remove(i)
        
    def set_current_host(self, ip, port):
        for i in hosts:
            if i.is_host(ip, port):
                self.current_host = i

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

    def shutdownhost(self):
        self.__send_cmd("exit")
                
