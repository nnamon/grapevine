#!/usr/bin/python

from fuzzd.gvfuzz import FuzzD
from fuzzd.gvcallingmechanisms import XNUCallingMechanism, TestCallingMechanism
from common.fuzzprofile.gvparser import GrapevineParser

UDP_IP="127.0.0.1"
UDP_PORT=10001
log_ip = "0.0.0.0"
log_port = 0
        
def main():
    # Get syscall profile first
    bsd_syscalls_master = "/home/jaybles/grapevine/grapevine/res/syscalls.master"
    mach_syscall_sw = "/home/jaybles/grapevine/grapevine/res/syscall_sw.c"

    # Obtain the syscall profile
    gp = GrapevineParser()
    syscall_profile = gp.parse(bsd_syscalls_master, mach_syscall_sw)

    # Create our fuzzd instance
    fuzzd = FuzzD("REPLACE ME", TestCallingMechanism(), syscall_profile, UDP_IP, UDP_PORT)
    fuzzd.listen()
    
if __name__ == "__main__":
    main()
