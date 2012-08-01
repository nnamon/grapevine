#!/usr/bin/python

import sys
import re
from host.gvhost import HostsController

def prompt():
    """Helper function"""
    try:
        sys.stdout.write( "ghost> ")
        uin = raw_input().rstrip()
        return uin
    except KeyboardInterrupt:
        return "SIGINT"


def logger(port,udp_ip,udp_port):
    """UDP Logging function, writes to file"""
    print "Logger spawned"
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.bind( ('0.0.0.0',port) )
    print "Port Bound",port
    filename = str(int(time()))
    f = open( filename, 'w')
    f.write("HOSTIP: ")
    f.write(udp_ip)
    f.write(" HOSTPORT: ")
    f.write(str(udp_port))
    f.write(" Logger port ")
    f.write(str(port))
    f.write("\n")
    f.close()
    while True:
        f = open(filename, 'a')
        data, addr = sock.recvfrom( 3072 )
        f.write(data)
        f.write("\nNEWSET\n")
        f.close()

def unable_to_connect_callback():
    print "Unable to connect."

def __handle(msg, ghost):
    msg = msg.strip()
    
    # Warning: Ugly regex ahead.
    con_match = re.compile("connect\s+((?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s+(\d+)").match(msg)
    log_match = re.compile("log\s+((?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s+(\d+)").match(msg)

    if con_match:
        ghost.connect(con_match.group(1), con_match.group(2))
        print "Connecting to %s:%d." % (con_match.group(1), 
                                        int(con_match.group(2)))
    elif log_match:
        ghost.set_log(log_match.group(1), log_match.group(2))
        print "Logging to %s:%d." % (ghost.log_ip, ghost.log_port)
    elif msg == "fuzz":
        print "Fuzzing %s:%d." % (ghost.current_host.ip, 
                                 ghost.current_host.port)
        ghost.current_host.fuzz()
    elif msg == "stopfuzz":
        print "We stopped fuzzing %s:%d." % (ghost.current_host.ip, 
                                            ghost.current_host.port)
        ghost.current_host.stopfuzz()
    elif msg == "dumpstate":
        pass
    elif msg == "loadgen":
        pass
    elif msg == "shutdown":
        ghost.shutdownhost()
        print "We shut down %s:%d. Removed from tracking." % (ghost.current_host_ip, ghost.current_host_port)
    elif msg == "help":
        sys.stdout.write( "Grapevine Host Control alpha\nCommands:\n\tcurrenthost:\t displays IP and PORT of currently connected HOST\n\tconnect:\t prompts for new connection details\n\tfuzz:\t\t start fuzzing in the connected host.\n\texit:\t\t exits the program.\n\tstopfuzz:\t\t Stops fuzzing.\n\tdumpstate:\t\t Stuff.\n\tloadgen:\t\tStuff.\n\thelp:\t\t Prints this help message.\n" )
    elif msg == "SIGINT":
        ghost.safe_exit("Interrupt signal detected, terminating program.")
    else:
        sys.stdout.write("Command not supported\n")        

def main():
    ghost = HostsController()

    while True:
        msg = prompt()
        __handle(msg, ghost)

if __name__ == "__main__":
    main()

