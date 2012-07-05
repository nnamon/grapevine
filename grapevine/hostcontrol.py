import socket
import sys

udp_ip="127.0.0.1"
udp_port=10001

def prompt():
    sys.stdout.write( "command> ")
    uin = raw_input()
    return uin

def set_connection(ip,port):
    global udp_ip 
    udp_ip = ip
    global udp_port 
    udp_port = port

if __name__ == "__main__":
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    #print "Fuzzd IP: ", UDP_IP
    #print "Fuzzd Port: ", UDP_PORT
    while True:
        msg = prompt()
        #if fuzzing, program should fork a new udp listener at a specific port, and send the details to fuzzd for logging.
        if msg == "currentvm":
            print "Current VM ip:",udp_ip
            print "Current VM port:",udp_port
        if msg == "connect":
            sys.stdout.write( "Input IP address of VM to send commands to> ")
            ip = raw_input().rstrip()
            sys.stdout.write( "Input port> ")
            port = raw_input().rstrip()
            set_connection( ip, int(port) )
        if msg == "exit":
            print "Exiting"
            sock.sendto(msg, ( udp_ip, udp_port ) )
            exit()
        if msg == "help":
            sys.stdout.write( "Grapevine Host Control alpha\nCommands:\n\tcurrentvm:\t displays IP and PORT of currently connected VM\n\tconnect:\t prompts for new connection details\n\texit:\t\t exits the program.\n\thelp:\t\t Prints this help message.\n" )
        print "Send: ", msg
        sock.sendto( msg, (udp_ip, udp_port) )
