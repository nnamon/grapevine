#calls syscall using libc

from ctypes import *

libc = cdll.LoadLibrary("libc.dylib")

scallnum = 0 #syscall number
validinput = 0 #valid input that syscall takes

libc.syscall(scallnum, validinput)

##example, chmod
#15 is AUE_CHMOD in BSD/XNU, 0644 is the chmod mask thing
libc.syscall(15, "/Users/yuuko/examples.desktop", 0644)
