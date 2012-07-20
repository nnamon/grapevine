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
