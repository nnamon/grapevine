import signal
import sys

def signal_caught(a, b):
    print "SIGNAL WORKED"
    print a
    print b
    sys.exit()

signal.signal(signal.SIGINT, signal_caught)

while True:
    pass
