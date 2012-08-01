#!/bin/usr/python

# Template abstract class Generator
# MUST BE SUBCLASSED to implement a generator.
# All functions should be overriden and implemented.
class Generator:
    profile = None
    state = None
    seed = None
    
    # Initialise the class with a seed value to kick start the generator.
    def __init__(self, profile, seed):
        self.profile
        self.seed = seed

    # Call getNext() to obtain the next set of inputs.
    # Should always return a list of values (Data should be expected by the syscall
    # calling mechanism).
    def getNext(self):
        raise Exception("Unimplemented getNext() in template Generator class.")

    # Call this function with a list of return values after fuzz input is run
    # to affect the state of the Generator in order to dynamically generate
    # input based on complex rules.
    # data is always a list of values.
    def affectState(self, data):
        raise Exception("Unimplemented affectState() in template Generator class.")


# Default generator
class DefaultGenerator(Generator):
    
    state = 0
    
    def getNext(self):
        return [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def affectState(self, data):
        self.state = self.state + 1
        print "Generator got %s back. (State %d)" % (data, self.state)


# Syscall Profile Use Generator
class XNUIntellect(Generator):
    """A generator designed to make use of syscall list parsing and intelligent filtering of unusable syscalls and their orders."""
    def getNext(self):
        pass

    def affectState(self, data):
        pass


import random
import binascii
class RandomFI(Generator):
    profile = None
    state = None
    seed = None
    
    def __init__(self, profile, seed):
        self.state = 0
        pass

    def getNext(self):
        args = []
        args.append(self.__getsyscall())
        for _ in range(0,8):
            args.append(self.__getarg())
        return args

    def affectState(self, data):
        self.state = self.state + 1
        print "Generator got %s back. (State %d)" % (data, self.state)

    def __getsyscall(self):
        ignore = [8, 11, 17, 19, 21, 22, 38, 40, 45, 62, 63, 64, 67,
                  68, 69, 70, 71, 72, 76, 77, 84, 87, 88, 91, 94, 99,
                  101, 102, 103, 107, 108, 109, 110, 112, 113, 114,
                  115, 119, 125, 129, 130, 141, 143, 144, 145, 146,
                  148, 149, 150, 156, 160, 162, 163, 164, 166, 168,
                  170, 171, 172, 174, 175, 177, 178, 179, 186, 193,
                  198, 213, 214, 215, 216, 217, 218, 219, 224, 246,
                  249, 257, 312, 321, 323, 326, 335, 352, 373, 374,
                  375, 376, 377, 378, 379, 401, 402, 403, 404, 409,
                  413, 418, 419, 423, 432, 433,
                  0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13,
                  -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25,
                  -30, -40, -41, -42, -47, -50, -54, -55, -56, -57, -63, -64,
                  -65, -66, -67, -68, -69, -70, -71, -72, -73, -74, -75, -76,
                  -77, -78, -79, -80, -81, -82, -83, -84, -85, -86, -87, -88,
                  -95, -96, -97, -98, -99, -100]

        while True:
            random.seed(self.__getseed())
            temp_sys = random.randint(-100, 433)
            if temp_sys not in ignore:
                return temp_sys

    def __getseed(self):
        return int(binascii.hexlify(open("/dev/urandom", "r").read(5).rstrip()),16)

    def __getrand(self):
        random_file = open('/dev/urandom', 'r')
        data = random_file.read(128).rstrip()
        random_file.close()
        return data

    def __getnumber(self):
        state = random.randrange(0,5)
        if state == 0:
            random.seed(1)
            return random.randrange(2147483647)
        elif state == 1:
            random.seed(1)
            # C-like random
            return (0xffffff00 | (random.randrange(2147483647) % 256)) 
        elif state == 2:
            return 0x8000
        elif state == 3:
            return 0xffff
        elif state == 4:
            return 0x80000000

    def __getarg(self):
        state = random.randrange(0,5)
        if state == 0:
            return 0x0804fd00 #userland addr
        elif state == 1:
            return 0x0000a000 #unmapped addr
        elif state == 2:
            return 0xc01fa0b6 #kernel addr, a guess
        elif state == 3:
            return self.__getnumber() #some number
        elif state == 4:
            return self.__getrand()
