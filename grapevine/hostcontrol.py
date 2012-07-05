import socket
import sys

UDP_IP="127.0.0.1"
UDP_PORT=5000

def prompt():
    sys.stdout.write( "command> ")
    uin = raw_input()
    return uin

if __name__ == "__main__":
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    print "Fuzzd IP: ", UDP_IP
    print "Fuzzd Port: ", UDP_PORT
    while True:
        msg = prompt()
        #if fuzzing, program should fork a new udp listener at a specific port, and send the details to fuzzd for logging.
        if msg == "exit":
            print "Exiting"
            exit()
        print "Send: ", msg
        sock.sendto( msg, (UDP_IP, UDP_PORT) )
