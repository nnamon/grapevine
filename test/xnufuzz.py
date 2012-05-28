from ctypes import *
import random
import binascii
from time import sleep
libc = cdll.LoadLibrary("libc.dylib")


#This ignore list is customized for xnu-1486.2.11 (10.6.2).

ignore = [
	8, 11, 17, 19, 21, 22, 38, 40, 45, 62, 63, 64, 67, 
    68, 69, 70, 71, 72, 77, 84, 87, 88, 91, 94, 99, 101, 
    102, 103, 107, 108, 109, 110, 112, 113, 114, 115, 119, 125, 129, 130, 
    141, 143, 144, 145, 146, 148, 149, 150, 156, 160, 162,
    163, 164, 166, 168, 170, 171, 172, 174, 175, 177, 178,
    179, 186, 193, 198, 213, 214, 215, 224, 246, 249, 257,
    312, 321, 323, 326, 335, 352, 373, 374, 375, 376, 377,
    378, 379
]

def getseed():
	return int(binascii.hexlify(open("/dev/urandom", 'r').read(5).rstrip()),16)

def getrand():
    f = open('/dev/urandom', 'r')
    d = f.read(128).rstrip()
    f.close()
    return d

def getnumber():
    state = random.randrange(0,5)
    #case statement goes here, lol python doesnt have switch
    if state == 0:
	    random.seed(1)
	    return random.randrange(2147483647)
    elif state == 1:
	    random.seed(1)
	    return (0xffffff00 | (random.randrange(2147483647) % 256)) #C-like random
    elif state == 2:
	    return 0x8000
    elif state == 3:
	    return 0xffff
    elif state == 4:
	    return 0x80000000

def getarg():
    state = random.randrange(0,5)
    b = ''
    if state == 0:
	    return 0x0804fd00 #userland addr
    elif state == 1:
	    return 0x0000a000 #unmapped addr
    elif state == 2:
	    return 0xc01fa0b6 #kernel addr, a guess
    elif state == 3:
	    return getnumber() #some number
    elif state == 4:
	    return getrand()

def memfuzz():
    arg = []
    syscallnr = 0
    flag = 1
    while True:
        flag = 1
        while not flag == 0:
            flag = 0
            random.seed(getseed())
            syscallnr = (random.randrange(2147483647) % 253)
            for i in ignore:
                if(i == syscallnr):
                    flag = 1
                    break
    
        for i in range(0,8):
           arg.append(getarg())

        print('syscall({}, {}, {}, {}, {}, {}, {}, {}, {})\n').format(syscallnr, arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7])
        sleep(5/1000000.0)
        returnVal = libc.syscall(syscallnr, arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7])
        print "return: ", returnVal
        
if __name__ == "__main__":
    memfuzz()
