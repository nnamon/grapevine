#!/usr/bin/python

from fuzzd.gvfuzz import FuzzD
from fuzzd.gvcallingmechanisms import XNUCallingMechanism, TestCallingMechanism
from common.fuzzprofile.gvparser import GrapevineParser
from fuzzlogger.gvlogger import LoggerClient

UDP_IP="0.0.0.0"
UDP_PORT=10001
log_ip = "127.0.0.1"
log_port = 5001
        
def main():
    #change paths accordingly
    # Get syscall profile first
    bsd_syscalls_master = "/home/jaybles/grapevine/grapevine/res/syscalls.master"
    mach_syscall_sw = "/home/jaybles/grapevine/grapevine/res/syscall_sw.c"

    # Obtain the syscall profile
    gp = GrapevineParser()
    syscall_profile = gp.parse(bsd_syscalls_master, mach_syscall_sw)

    # New Logger
    logger = LoggerClient(log_ip, log_port)
    
    #change TestCallingMechanism to XNUCallingMechanism() for fuzzing
    # Create our fuzzd instance
    fuzzd = FuzzD(logger, TestCallingMechanism(), syscall_profile, UDP_IP, UDP_PORT)
    fuzzd.listen()
    
if __name__ == "__main__":
    main()
