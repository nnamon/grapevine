from ctypes import *
import random
import socket
import time
import json
import binascii
from time import sleep
import fuzzmod.randomFI
from threading import Timer
from threading import Thread
randomFI = fuzzmod.randomFI()
#libc = cdll.LoadLibrary("libc.dylib")
UDP_IP="127.0.0.1"
UDP_PORT=10001
log_ip = "0.0.0.0"
log_port = 0

#This ignore list is customized for xnu-1504.9.37 (10.6.7).

ignore = [
	8, 11, 17, 19, 21, 22, 38, 40, 45, 62, 63, 64, 67, 
    68, 69, 70, 71, 72, 76, 77, 84, 87, 88, 91, 94, 99, 101, 
    102, 103, 107, 108, 109, 110, 112, 113, 114, 115, 119, 125, 129, 130, 
    141, 143, 144, 145, 146, 148, 149, 150, 156, 160, 162,
    163, 164, 166, 168, 170, 171, 172, 174, 175, 177, 178,
    179, 186, 193, 198, 213, 214, 215, 216, 217, 218, 219,
    224, 246, 249, 257,
    312, 321, 323, 326, 335, 352, 373, 374, 375, 376, 377,
    378, 379, 401, 402, 403, 404, 409, 413, 418, 419, 423, 432, 433,
    0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13,
    -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25,
    -30, -40, -41, -42, -47, -50, -54, -55, -56, -57, -63, -64,
    -65, -66, -67, -68, -69, -70, -71, -72, -73, -74, -75, -76,
    -77, -78, -79, -80, -81, -82, -83, -84, -85, -86, -87, -88,
    -95, -96, -97, -98, -99, -100
]

def logit(syscallnr, arg):
    """Logging to UDP listener. Sends a JSON string with syscall numbers and arguments. Arguments and hexlifyied."""
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    payload = json.dumps({"syscallnr": syscallnr, "arg1": binascii.hexlify(arg[0]), "arg2": binascii.hexlify(arg[1]), "arg3": binascii.hexlify(arg[2]), "arg4": binascii.hexlify(arg[3]), "arg5": binascii.hexlify(arg[4]), "arg6": binascii.hexlify(arg[5]), "arg7": binascii.hexlify(arg[6]), "arg8": binascii.hexlify(arg[7])},ensure_ascii=True)
    sock.sendto( payload, (log_ip, log_port) )
    

def memfuzz():
    arg = []
    syscallnr = 0
    flag = 1
    while True:
        flag = 1
        while not flag == 0:
            flag = 0
            random.seed(randomFI.getseed())
            syscallnr = random.randint(-100, 433)
            for i in ignore:
                if(i == syscallnr):
                    flag = 1
                    break
    
            arg = randomFI.getargs()
            logit(syscallnr,arg)
            #print('syscall({}, {}, {}, {}, {}, {}, {}, {}, {})\n').format(syscallnr, arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7])
            sleep(5/1000000.0)
            #returnVal = libc.syscall(syscallnr, arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7])
            #print "return: ", returnVal

def checkFuzz(thread):
    print "Checking"
    if thread.isAlive() is False:
        fuzzing = Thread(target=memfuzz, name="fuzz")
        fuzzing.start()
    else:
        print "Thread is alive"
        

    
if __name__ == "__main__":
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.bind ( (UDP_IP,UDP_PORT) )
    print "Socket binding success. Listening on",UDP_PORT
    while True:
        data, addr = sock.recvfrom( 1024 ) #buffer 1024
        print "Instructs: ",data
        print "From: ",addr
        if data == 'fuzz':
            global log_ip
            log_ip = addr
            global log_port
            log_port = sock.recvfrom( 512 ) #recv log port
            fuzzing = Thread(target=memfuzz,name="fuzz")
            fuzzing.start()
            checker = Timer(30.0, checkFuzz, [fuzzing])
            checker.start()
        if data == "exit":
            exit()
