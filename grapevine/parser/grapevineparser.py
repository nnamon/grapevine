#!/usr/bin/python
import re

class Syscall:
    pass

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
    
class SyscallsProfile:
    bsd_syscalls = None
    mach_syscalls = None
    rules = None

    def __init__(self, bsd_syscalls = [], mach_syscalls = [], rules = []):
        self.bsd_syscalls = bsd_syscalls
        self.mach_syscalls = mach_syscalls
        self.rules = rules

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

class GrapevineParser:
    
    def parse_bsdsyscalls(self, filename):
        syscall_collection = BSDSyscallsCollection()
        parse_strings = [i.strip() for i in file(filename).read().splitlines()]
        syscall_pattern = re.compile(r"(\d+)\s+(\w+)\s+(ALL|[TNHP]{1,4}|UALL|UHN)\s+{\s+(\w+)\s+(\w+)\((.+)\)(?:\s+(NO_SYSCALL_STUB)\s*)?;\s+}(?:\s+{\s+(.+)\s+})?")
        option_patterns= {"if": re.compile(r"#if (\w+)"),
                          "else": re.compile(r"#else.*"), 
                          "endif": re.compile(r"#endif.*")}
        current_branch = "default"
        current_else = False
        
        for i in parse_strings:
            syscalldef_match = syscall_pattern.match(i)

            option_match = None
            option_index = ""
            for p in option_patterns.keys():
                option_match = option_patterns[p].match(i)
                if option_match:
                    option_index = p
                    
            if option_index == "if":
                current_branch = option_match.group(1)
            elif option_index == "else":
                current_else = True
            elif option_index == "endif":
                current_branch = "default"
                current_else = False
            elif syscalldef_match:
                number = syscalldef_match.group(1)
                audit_event = syscalldef_match.group(2)
                in_files = syscalldef_match.group(3)
                comments = syscalldef_match.group(8) or "No comments"

                # Construct the function prototype object
                func_rettype = syscalldef_match.group(4)
                func_name = syscalldef_match.group(5)
                syscall_stub = (True if syscalldef_match.group(7) == "NO_SYSCALL_STUB" or func_name[0:2] == "__" else False)
                function_prototype = BSDSyscallFunctionPrototype(func_rettype, func_name, syscall_stub)
                argument_pattern = re.compile("(.+)\s+(.+)")
                if not syscalldef_match.group(6) == "void":
                    for j in [k.strip() for k in syscalldef_match.group(6).split(",")]:
                        arg_split = argument_pattern.match(j)
                        function_prototype.add_argument(arg_split.group(1), arg_split.group(2))
                        
                # Adding the syscall to the collection
                new_bsdsyscall = BSDSyscall(function_prototype, number, audit_event, in_files, comments)
                syscall_collection.add_syscall(new_bsdsyscall, current_branch, current_else)
                
        return syscall_collection


if __name__ == "__main__":
    g = GrapevineParser()
    a = g.parse_bsdsyscalls("../res/syscalls.master")
    print a.syscall_tree['default']
