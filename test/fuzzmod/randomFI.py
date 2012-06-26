import random
import binascii

class randomFI:
    def getseed(self):
        return int(binascii.hexlify(open("/dev/urandom", 'r').read(5).rstrip()),16)

    def getrand(self):
            f = open('/dev/urandom', 'r')
            d = f.read(128).rstrip()
            f.close()
            return d

    def getnumber(self):
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

    def getarg(self):
           state = random.randrange(0,5)
           b = ''
           if state == 0:
               return 0x0804fd00 #userland addr
           elif state == 1:
              return 0x0000a000 #unmapped addr
           elif state == 2:
              return 0xc01fa0b6 #kernel addr, a guess
           elif state == 3:
              return self.getnumber() #some number
           elif state == 4:
              return self.getrand()

    def getargs(self):
        arg = []
        for i in range(0,8):
            arg.append(self.getarg())
        return arg
