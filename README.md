grapevine OSX XNU Kernel Fuzzer
===============================
Mac OSX/Darwin Kernel Automated Fuzzer Generator.
-------------------------------------------------

##Aims
 - Automatically parses syscall files/headers to generate fuzz input.
    - Dynamic, if there are new or removed syscalls, fuzzer will change accordingly.
 - Modular
    - different fuzzing techniques
 - Extensible 
    - Write parsers to parse syscalls from other kernels (Linux/BSD/etc)
    
##Program Flow
Refer to [parseflow](https://github.com/jergorn93/grapevine/blob/master/grapevine/res/parseflow)
