#!/usr/bin/python

# Calling Mechanisms

# Abstract class, needs to be implemented.
class CallingMechanism:
    
    def call(self, syscall_number, *args):
        raise Exception("Unimplemented call() in abstract CallingMechanism class.")

# Calling mechanism used for this project    
class XNUCallingMechanism(CallingMechanism):
    
    def call(self, syscall_number, *args):
        """Takes in a syscall number and a list or tuple of arguments"""
        returnVal = libc.syscall(syscall_number, *args)
        return returnVal
