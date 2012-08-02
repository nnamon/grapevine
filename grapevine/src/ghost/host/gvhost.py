#/usr/bin/python

import socket
import select
from threading import Thread
import time
import signal
import sys

class Host:
    """Host does monitoring of the host and allows control through callbacks."""
    # Instance Variables
    ip = "127.0.0.1"
    port = 10001
    state =  0 # Uninitialised
    sock = None
    callback_set = {}
    mon_timeout = 0.02
    mon_ticks = 0
    mon_pings_missed = 0

    # Constants
    UNINITIALISED = 0
    CONNECTED = 1
    WAITING_FOR_PING = 2
    LOST_CONNECTION = 3
    TERMINATED = -1
    UNCONNECTED = -2

    def __init__(self, ip, port, callback_set = {}):
        self.ip = ip
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        if callback_set == {}:
            self.callback_set = {
                'unable_to_connect': self.__default_unable_to_connect_callback,
                'lost_connection':  self.__default_lost_connection_callback,
                'data_received':  self.__default_data_received_callback,
                'reconnected':  self.__default_reconnected_callback,
                'connected': self.__default_connected_callback,
                }
        else:
            self.callback_set = callback_set

            
    # Internal host functions

    def __send_cmd(self, data):
        self.sock.sendto(data, (self.ip, self.port))

    def __call_callback(self, event, *args):
        self.callback_set[event](*args)

    @staticmethod
    def __default_lost_connection_callback(addr):
        print "Advice: Lost connection event is not handled."

    @staticmethod
    def __default_unable_to_connect_callback(addr):
        print "Advice: Unable to connect event is not handled."

    @staticmethod
    def __default_reconnected_callback(addr):
        print "Advice: Reconnected event is not handled."

    @staticmethod
    def __default_connected_callback(addr):
        print "Advice: Connected event is not handled."

    @staticmethod
    def __default_data_received_callback(addr, data):
        print "\nData is Received:\n", data

    def start(self):
        Thread(target=self.monitor, name="monitor").start()
        self.hello()

    def monitor(self):
        """Run in a separate thread to block on select calls. On the first run the timeout is set to 5 seconds, otherwise it takes a minute to timeout. Pings should be sent every 2 seconds so if there is no response in a minute, it is assumed that a crash has occured and the crash_detected callback will be called. On the first run, it will call the unable_to_connect callback."""
        while self.state >= 0:
            self.mon_ticks = self.mon_ticks + 1
            ready = select.select([self.sock], [], [], self.mon_timeout)
            if ready[0]:
                data = self.sock.recv(4092)
                self.__handle(data)
                ready = None
            self.__tick_check()

    def __tick_check(self):
        ticks_per_sec = 1/self.mon_timeout
        secs_elapsed = self.mon_ticks/ticks_per_sec
        if secs_elapsed > 5.0 and self.state == self.UNINITIALISED:
            self.__call_callback("unable_to_connect", 
                                 (self.ip, self.port))
            self.state = self.UNCONNECTED
        if secs_elapsed % 2 == 0:
            self.ping()
            if self.state == self.CONNECTED:
                self.state = self.WAITING_FOR_PING
        if self.state == self.WAITING_FOR_PING:
            self.mon_pings_missed = self.mon_pings_missed + 1
        if (self.mon_pings_missed/(1/self.mon_timeout)) > 5 and self.state == self.WAITING_FOR_PING:
            self.__call_callback("lost_connection", (self.ip, self.port))
            self.state = self.LOST_CONNECTION

    def __handle(self, data):
        self.__call_callback('data_received', (self.ip, self.port), data)
        if data.startswith("hello from "):
            self.state = self.CONNECTED
            self.__call_callback("connected", (self.ip, self.port))
            self.mon_pings_missed = 0
        elif data == "pong":
            if self.state == self.WAITING_FOR_PING:
                self.state = self.CONNECTED
            elif self.state == self.LOST_CONNECTION:
                self.state = self.UNINITIALISED
                self.__call_callback("reconnected", (self.ip, self.port))
                self.mon_ticks = 0
                self.hello()
            self.mon_pings_missed = 0

    def stop(self):
        self.state = self.TERMINATED
        
    def is_host(self, ip, port):
        if self.ip == ip and self.port == int(port):
            return True
        else:
            return False

    # Command sending functions

    def shutdown(self):
        self.__send_cmd("exit")
        self.state = self.TERMINATED

    def bye(self):
        self.__send_cmd("bye")

    def hello(self):
        self.__send_cmd("hello")

    def ping(self):
        self.__send_cmd("ping")

    def fuzz(self):
        self.__send_cmd("fuzz")

    def stopfuzz(self):
        self.__send_cmd("stopfuzz")

    def loadgen(self, gen_name, seed, code):
        self.__send_cmd("loadgen")
        self.__send_cmd(gen_name)
        self.__send_cmd(seed)
        self.__send_cmd(code)

    def log(self, ip, port):
        self.__send_cmd("%s %d" % (ip, int(port)))

    def dumpstate(self):
        self.__send_cmd("dumpstate")

class HostsController:
    hosts = [] # A list of Hosts
    log_ip = "127.0.0.1" # Externally accessible host IP address.
    log_port = 5000
    sock = None
    current_host = None
    callbacks = {}
    
    def __init__(self, hosts = [], log_ip = "127.0.0.1", log_port = 5000, callbacks = {}):
        # hosts is to be a list of tuples in the form (addr, port)
        for i in hosts:
            ip, port = i
            self.add_new_host(ip, port)
        self.log_ip = log_ip
        self.log_port = log_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.callbacks = callbacks

    def connect(self, ip, port):
        new_host = True
        for i in self.hosts:
            if i.is_host(ip, port):
                new_host = False
        if new_host:
            self.add_new_host(ip, port)
        self.set_current_host(ip, port)

    def add_new_host(self, ip, port):
        for i in self.hosts:
            if i.is_host(ip, port):
                return False
        new_host = Host(ip, port, self.callbacks)
        self.hosts.append(new_host)
        new_host.start()

    def remove_host(self, ip, port):
        for i in self.hosts:
            if i.is_host(ip, port):
                i.stop()
                if i == self.current_host:
                    self.remove_current_host
                else:
                    self.hosts.remove(i)

    def remove_current_host(self):
        self.hosts.remove(self.current_host)
        self.current_host = None

    def set_current_host(self, ip, port):
        for i in self.hosts:
            if i.is_host(ip, port):
                self.current_host = i

    def set_log(self, ip, port):
        self.log_ip = ip
        self.log_port = int(port)
        # Inform all hosts.

    def __interrupt_handler(self, sig_no, stack_frame):
        self.__safe_exit("Interrupt signal detected, terminating program.")
        
    # Ensuring a thread safe exit.
    def safe_exit(self, reason):
        print reason
        for i in self.hosts:
            i.bye()
            i.state = Host.TERMINATED
        time.sleep(0)
        sys.exit()
