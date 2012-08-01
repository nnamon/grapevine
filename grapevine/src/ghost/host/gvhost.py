#/usr/bin/python

import socket
import select

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
    TERMINATED = -1

    def __init__(self, ip, port, callback_set = {}):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if callback_set == {}:
            callback_set['unable_to_connect'] = self.__default_unable_to_connect_callback
            callback_set['crash_detected'] =  self.__default_crash_detected_callback
        self.start()

    def __send_cmd(self, data):
        self.sock.sendto(data, (self.current_host.ip, self.current_host.port))

    @staticmethod
    def __default_crash_detected_callback():
        print "Crash detected event is not handled."

    @staticmethod
    def __default_unable_to_connect_callback():
        print "Unable to connect event is not handled."

    def start():
        pass

    def monitor():
        """Run in a separate thread to block on select calls. On the first run the timeout is set to 5 seconds, otherwise it takes a minute to timeout. Pings should be sent every 2 seconds so if there is no response in a minute, it is assumed that a crash has occured and the crash_detected callback will be called. On the first run, it will call the unable_to_connect callback."""

        self.mon_callback = self.callback_set['unable_to_connect']
        self.mon_timeout = 5
        
        while self.state != self.TERMINATED:
            ready = None
            ready = select.select([self.socket], [], [], self.mon_timeout)
            if ready[0]:
                data = self.socket
                self.mon_callback = self.callback_set['crash_detected']
                self.mon_timeout = 60
            else:
                self.mon_callback()
                break

    def stop():
        self.state = self.TERMINATED

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
                
