#!/usr/bin/python

import socket
import pickle
import json

class LoggerClient:
    """Simple logging over the network."""

    log_ip = None
    log_port = None
    sock = None

    def __init__(self, log_ip, log_port):
        self.log_ip = log_ip
        self.log_port = log_port
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

    def log_syscall(self, syscallnr, *arg):
        """Logging to UDP listener. Sends a JSON string with syscall numbers and arguments. Arguments and hexlifyied."""
        prepayload = {"syscall_number": syscallnr}
        for i in range(0, len(arg)):
            prepayload["arg%d" % i] = pickle.dumps(arg[i])
        payload = json.dumps(prepayload, ensure_ascii=True)
        self.__dgram_send(payload)

    def log_return(self, retVal):
        """Sends return value of syscall to logger."""
        payload = json.dumps({"return_value": str(retVal)}, ensure_ascii=True)
        self.__dgram_send(payload)

    def log_event(self, event, urgency):
        """Sends a string describing an event and sets its urgency type"""
        payload = json.dumps({"event": event, "urgency": urgency}, ensure_ascii=True)
        self.__dgram_send(payload)

    def __dgram_send(self, payload):
        sock.sendto(payload, (self.log_ip, self.log_port))
