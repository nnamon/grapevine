#!/bin/usr/python

# Abstract class Generator
# ! Should be subclassed when used in an implementation !
# All functions should be overriden and implemented.
class Generator:
    profile = None
    state = None

    def generator(self):
        raise Exception("Unimplemented generator() in abstract Generator class.")

    # Call getNext() to obtain the next set of inputs.
    # Should always return a list of values.
    def getNext(self):
        raise Exception("Unimplemented getNext() in abstract Generator class.")

    # Call this function with a list of return values after fuzz input is run
    # to affect the state of the Generator in order to dynamically generate
    # input based on complex rules.
    def affectState(self):
        raise Exception("Unimplemented affectState() in abstract Generator class.")
