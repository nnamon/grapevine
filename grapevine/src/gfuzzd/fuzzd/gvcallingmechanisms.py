#!/usr/bin/python

# Calling Mechanisms

# Abstract class, needs to be implemented.
class CallingMechanism:
    
    def call(self, syscall_number, *args):
        raise Exception("Unimplemented call() in abstract CallingMechanism class.")

# Calling mechanism used for this project   
# UNCOMMENT OUT THE FOLLOWING LINES TO RUN IN A MAC OS X ENVIRONMENT
# from ctypes import *
# libc = cdll.LoadLibrary("libc.dylib")
class XNUCallingMechanism(CallingMechanism):
    
    def call(self, syscall_number, *args):
        """Takes in a syscall number and a list or tuple of arguments"""
        returnVal = libc.syscall(syscall_number, *args)
        return returnVal

# Calling mechanism to test input handling.
class TestCallingMechanism(CallingMechanism):
    
    def call(self, syscall_number, *args):
        print "We called syscall %s with arguments: %s" % (syscall_number, args)
        returnVal = syscall_number
        return returnVal
