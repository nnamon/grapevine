import socket
import sys
import re
from threading import Thread
from time import time

udp_ip="127.0.0.1"
udp_port=10001
log_listeners = [4999]
loggers = []

def parse():
    """Function to make use of the parser."""
    pass

def prompt():
    """Helper function"""
    sys.stdout.write( "command> ")
    uin = raw_input().rstrip()
    return uin

def set_connection(ip,port):
    """Set currently targetted VM"""
    global udp_ip 
    udp_ip = ip
    global udp_port 
    udp_port = port

def logger(port,udp_ip,udp_port):
    """UDP Logging function, writes to file"""
    print "Logger spawned"
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.bind( ('0.0.0.0',port) )
    print "Port Bound",port
    filename = str(int(time()))
    f = open( filename, 'w')
    f.write("VMIP: ")
    f.write(udp_ip)
    f.write(" VMPORT: ")
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
        

if __name__ == "__main__":
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    #print "Fuzzd IP: ", UDP_IP
    #print "Fuzzd Port: ", UDP_PORT
    ipregex = re.compile('\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', re.VERBOSE)
    portregex = re.compile('\b\d{1,5}\b')
    while True:
        msg = prompt()
        #if fuzzing, program should fork a new udp listener at a specific port, and send the details to fuzzd for logging.
        print "Msg:",msg
        #sock.sendto( msg, ( udp_ip, udp_port ) )
        if msg == "currentvm":
            print "Current VM ip:",udp_ip
            print "Current VM port:",udp_port
        elif msg == "connect":
            badport = True
            badip = True
            while badip:
                sys.stdout.write( "Input IP address of VM to send commands to> ")
                ip = raw_input().rstrip()
                try:
                    socket.inet_aton(ip)
                    badip = False
                except socket.error:
                    badip = True
                
            while badport:
                sys.stdout.write("Input port> ")
                port = raw_input().rstrip()
                if re.match('\d{1,5}',port) and len(port) < 6:
                    badport = False
                else:
                    badport = True
            set_connection( ip, int(port) )
        elif msg == "parse":
            sys.stdout.write("Do some parsing, get some values\n")
        elif msg == "fuzz":
            print "Fuzzing:",udp_ip
            sock.sendto( msg, (udp_ip, udp_port) ) #send "fuzz"
            #fork udp logger listener
            #global log_listeners
            log_listeners.append(log_listeners[len(log_listeners)-1]+1) #add new port to list
            port = log_listeners[len(log_listeners)-1] #same value as above
            sock.sendto( str(port), (udp_ip,udp_port) ) #send logger port
            logging = Thread( target=logger, args=([port,udp_ip,udp_port]) )
            logging.daemon = True
            loggers.append(logging)
            logging.start()
        elif msg == "exit":
            print "Exiting"
            sock.sendto(msg, ( udp_ip, udp_port ) )
            exit()
        elif msg == "help":
            sys.stdout.write( "Grapevine Host Control alpha\nCommands:\n\tcurrentvm:\t displays IP and PORT of currently connected VM\n\tconnect:\t prompts for new connection details\n\tfuzz:\t\t start fuzzing in the connected vm.\n\texit:\t\t exits the program.\n\thelp:\t\t Prints this help message.\n" )
        else:
            sys.stdout.write("Command not supported\n")
        
        
