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
    elif msg == "SIGINT":
        ghost.safe_exit("Interrupt signal detected, terminating program.")
    elif msg == "help":
        sys.stdout.write( "Grapevine Host Control alpha\nCommands:\n\tcurrenthost:\t displays IP and PORT of currently connected HOST\n\tconnect:\t prompts for new connection details\n\tfuzz:\t\t start fuzzing in the connected host.\n\texit:\t\t exits the program.\n\tstopfuzz:\t\t Stops fuzzing.\n\tdumpstate:\t\t Stuff.\n\tloadgen:\t\tStuff.\n\thelp:\t\t Prints this help message.\n" )
    elif ghost.current_host != None:
        if msg == "fuzz":
            print "Fuzzing %s:%d." % (ghost.current_host.ip, 
                                      ghost.current_host.port)
            ghost.current_host.fuzz()
        elif msg == "stopfuzz":
            print "We stopped fuzzing %s:%d." % (ghost.current_host.ip, 
                                                 ghost.current_host.port)
            ghost.current_host.stopfuzz()
        elif msg == "hoststatus":
            states = {
                '0': "UNINITIALISED",
                '1': "CONNECTED",
                '2': "WAITING_FOR_PING",
                '3': "LOST_CONNECTION",
                '-1': "TERMINATED",
                '-2': "UNCONNECTED",
                }
            for i in ghost.hosts:
                print "%s:%d - %s" % (i.ip, i.port, states[str(i.state)])
        elif msg == "loadgen":
            generator_name = raw_input("Generator Name: ")
            seed = raw_input("Seed: ")
            generator_file = raw_input("Generator File: ")
            try:
                generator_code = file(generator_file).read()
            except:
                print "Reading from %s has failed." % generator_file
            ghost.current_host.loadgen(generator_name, seed, generator_code)
        elif msg == "shutdown":
            ip = ghost.current_host.ip
            port = ghost.current_host.port
            ghost.current_host.shutdown()
            ghost.remove_current_host()
            print "We shut down %s:%d. Removed from tracking." % (ip, port)
        elif msg == "dumpstate":
            ghost.current_host.dumpstate()
        elif msg == "currenthost":
            sys.stdout.write("We are currently connected to %s:%d\n" % (ghost.current_host.ip, ghost.current_host.port))
        else:
            sys.stdout.write("Command not supported for this host.\n")
    else:
        sys.stdout.write("Connect to a host to continue.\n")

def __unable_to_connect_callback(addr):
    sys.stdout.write("\nError: We were unable to connect to %s:%d. Removing host from tracked hosts.\nghost> " % addr)
    ghost.remove_host(addr[0], addr[1])
    sys.stdout.flush()
    
def __lost_connection_callback(addr):
    sys.stdout.write("\nError: We lost our connection to %s:%d. Attempting to reconnect.\nghost> " % addr)
    sys.stdout.flush()

def __reconnected_callback(addr):
    sys.stdout.write("\nWe regained our connection to %s:%d.\nghost> " % addr)
    sys.stdout.flush()

def __connected_callback(addr):
    sys.stdout.write("\nSuccessfully connected to %s:%d.\nghost> " % addr)
    sys.stdout.flush()

def __data_received_callback(addr, data):
    if not data.startswith("hello") and not data == "pong":
        sys.stdout.write("\nNotice: We have received data from %s:%d.\n" % addr)
        sys.stdout.write("%s\nghost> " % data)
        sys.stdout.flush()

def main():
    callbacks = {
        'unable_to_connect': __unable_to_connect_callback,
        'lost_connection': __lost_connection_callback,
        'reconnected': __reconnected_callback,
        'data_received': __data_received_callback,
        'connected': __connected_callback,
        }

    global ghost 
    ghost = HostsController(callbacks=callbacks)

    while True:
        msg = prompt()
        __handle(msg, ghost)

if __name__ == "__main__":
    main()

