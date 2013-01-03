#!/usr/bin/python

import sys
import re
#from host.gvhost import HostsController
import threading
from logger.gvloglistener import LogListener
#import host.vm.vbcontrol as VBControl
#import host.vm.vbinfo as VBInformation
import time
def prompt():
    """Helper function"""
    try:
        sys.stdout.write( "ghost> ")
        uin = raw_input().rstrip()
        return uin
    except KeyboardInterrupt:
        return "SIGINT"


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
        logger.stop_logging() 
        ghost.safe_exit("Interrupt signal detected, terminating program.")
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
    elif msg == "help":
        sys.stdout.write( "Grapevine Host Control alpha\nCommands:\n\tcurrenthost:\t displays IP and PORT of currently connected HOST\n\tconnect:\t prompts for new connection details\n\tfuzz:\t\t start fuzzing in the connected host.\n\texit:\t\t exits the program.\n\tstopfuzz:\t\t Stops fuzzing.\n\tdumpstate:\t\t Stuff.\n\tloadgen:\t\tStuff.\n\thelp:\t\t Prints this help message.\n" )
    elif msg == "exit":
        logger.stop_logging()
        ghost.safe_exit("User exited, terminating program.")       
    elif ghost.current_host != None:
        if msg == "fuzz":
            print "Fuzzing %s:%d." % (ghost.current_host.ip, 
                                      ghost.current_host.port)
            ghost.current_host.fuzz()
        elif msg == "stopfuzz":
            print "We stopped fuzzing %s:%d." % (ghost.current_host.ip, 
                                                 ghost.current_host.port)
            ghost.current_host.stopfuzz()
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
    #Bad function that restarts VM even though connection has been regained.
    #vbi = VBInformation.Information()
    #vbc = VBControl.Controller()
    #dead = vbi.getCrashedMachines()
    #to implement grab system logs, track ip to vmid
    #if not dead:
    #    sys.stdout.write( "No dead machine. Lost connection due to network error or PANIC." )
    #    live = vbi.getAllLiveMachinesID()
    #    sys.stdout.write("Attempting fix.")
    #    if not live or live[0] == 0:
    #        sys.stdout.write("Network error")
    #    elif live == None:
    #        sys.stdout.write("Network error")
    #    else:
    #        for livemachineid in live:
    #            vbc.dumpGuestCore(livemachineid)
    #            time.sleep(30)
    #            vbc.shutdownMachine(livemachineid)
    #            time.sleep(30)
    #            vbc.activateMachine(livemachineid, True)
    #    sys.stdout.write("Restarting possible Panic machines. This will take some time ")
    #else:
    #    sys.stdout.write( "Restarting dead machines. " )
    #    for deadmachineid in dead:
    #        vbc.dumpGuestCore(deadmachineid)
    #        time.sleep(30)
    #        vbc.shutdownMachine(deadmachinemid)
    #        time.sleep(30)
    #        vbc.activateMachine(deadmachinemid, True)
    #        time.sleep(5)
    #        
    #    sys.stdout.write( "Restarting dead machines." )
   
    sys.stdout.flush()

def __reconnected_callback(addr):
    sys.stdout.write("\nWe regained our connection to %s:%d.\nghost> " % addr)
    sys.stdout.flush()

def __connected_callback(addr):
    sys.stdout.write("\nSuccessfully connected to %s:%d.\nghost> " % addr)
    sys.stdout.flush()

def __data_received_callback(addr, data):
    no_print = ['pong']
    if not data.startswith("hello") and not data.startswith("bye") and not data in no_print:
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

    global logger
    logger = LogListener("0.0.0.0", 5001)
    logger_thread = threading.Thread(target=logger.listen)
    logger_thread.start()

    global ghost 
    ghost = HostsController(callbacks=callbacks)

    while True:
        msg = prompt()
        __handle(msg, ghost)

if __name__ == "__main__":
    main()

