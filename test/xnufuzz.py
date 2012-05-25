from ctypes import *
import random
import binascii
libc = cdll.LoadLibrary("libc.dylib")


#This ignore list is customized for xnu-1486.2.11 (10.6.2).

ignore[] = [
	8, 11, 17, 19, 21, 22, 38, 40, 45, 62, 63, 64, 67, 
    68, 69, 70, 71, 72, 77, 84, 87, 88, 91, 94, 99, 101, 
    102, 103, 107, 108, 109, 110, 112, 113, 114 115, 119, 125, 129, 130, 
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
    #case statement goes here

def getarg():
    state = random.randrange(0,5)
    b = ''
