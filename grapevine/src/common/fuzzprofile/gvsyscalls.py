#!/usr/bin/python

# Syscall Base Class #

class Syscall:
    pass


# BSD Syscalls #

class BSDSyscall(Syscall):
    number = None # int, BSD Syscalls will never be less than 0.
    audit_event = None # string
    in_files = None # list
    function_prototype = None # BSDSyscallFunctionPrototype
    comments = None # string

    def __init__(self, function_prototype, number = -1, audit_event = "AUE_NULL", in_files = [], comments = ""):
        self.number = int(number)
        self.audit_event = audit_event
        self.in_files = in_files
        self.comments = comments
        self.function_prototype = function_prototype

    def __str__(self):
        return "%-10d %-15s %-15s {%s} {%s}" % (self.number, self.audit_event, self.in_files, self.function_prototype.__str__(), self.comments)

    def __repr__(self):
        return "<BSDSyscall: %d %s>" % (self.number, self.function_prototype.function_name)

class BSDSyscallFunctionPrototype:
    return_type = None # string
    function_name = None # string
    arguments = None # list of paired tuples
    nosyscall_stub = None # boolean
    
    def __init__(self, return_type, function_name, nosyscall_stub = False):
        self.return_type = return_type
        self.function_name = function_name
        self.arguments = []
        self.nosyscall_stub = nosyscall_stub

    def add_argument(self, data_type, name):
        self.arguments.append((data_type, name))

    def __str__(self):
        function_list = "".join("%s %s, " % (i,v) for i, v in self.arguments)[0:-2]
        return "%s %s(%s)%s;" % (self.return_type, self.function_name, (function_list if not function_list == "" else "void"), (" NO_SYSCALL_STUB" if self.nosyscall_stub else ""))

    def __repr__(self):
        return self.__str__()
    
class BSDSyscallsCollection:
    syscall_tree = {"default": []}
    
    def add_syscall(self, syscall, branch_name="default", else_branch=False):
        if branch_name == "default":
            if else_branch:
                return False # The default branch can never contain an else branch
            self.syscall_tree["default"].append(syscall)
            return True

        if branch_name not in self.syscall_tree:
            self.syscall_tree[branch_name] = {"default": [], "else": []}

        if else_branch:
            self.syscall_tree[branch_name]["else"].append(syscall)
            return True
        
        self.syscall_tree[branch_name]["default"].append(syscall)
        return True

# Mach Syscalls #

class MachSyscall(Syscall):
    pass

# Syscall Profile #

class SyscallProfile:
    bsd_syscalls = None
    mach_syscalls = None

    def __init__(self, bsd_syscalls, mach_syscalls):
        self.bsd_syscalls = bsd_syscalls
        self.mach_syscalls = mach_syscalls

