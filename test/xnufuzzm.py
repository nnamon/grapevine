from ctypes import *
import random
from time import sleep
import fuzzmod.randomFI
randomFI = fuzzmod.randomFI()
libc = cdll.LoadLibrary("libc.dylib")

#This ignore list is customized for xnu-1504.9.37 (10.6.7).

ignore = [
	8, 11, 17, 19, 21, 22, 38, 40, 45, 62, 63, 64, 67, 
    68, 69, 70, 71, 72, 77, 84, 87, 88, 91, 94, 99, 101, 
    102, 103, 107, 108, 109, 110, 112, 113, 114, 115, 119, 125, 129, 130, 
    141, 143, 144, 145, 146, 148, 149, 150, 156, 160, 162,
    163, 164, 166, 168, 170, 171, 172, 174, 175, 177, 178,
    179, 186, 193, 198, 213, 214, 215, 224, 246, 249, 257,
    312, 321, 323, 326, 335, 352, 373, 374, 375, 376, 377,
    378, 379, 401, 402, 403, 404, 409, 413, 418, 419, 423, 432, 433,
    0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13,
    -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25,
    -30, -40, -41, -42, -47, -50, -54, -55, -56, -57, -63, -64,
    -65, -66, -67, -68, -69, -70, -71, -72, -73, -74, -75, -76,
    -77, -78, -79, -80, -81, -82, -83, -84, -85, -86, -87, -88,
    -95, -96, -97, -98, -99, -100
]

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

        print('syscall({}, {}, {}, {}, {}, {}, {}, {}, {})\n').format(syscallnr, arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7])
        sleep(5/1000000.0)
        returnVal = libc.syscall(syscallnr, arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7])
        print "return: ", returnVal
        
if __name__ == "__main__":
    memfuzz()
