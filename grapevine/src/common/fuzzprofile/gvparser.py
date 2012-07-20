#!/usr/bin/python

from gvsyscalls import *
import re

class GrapevineParser:

    def parse(self, bsd_file):
        bsd_syscalls = self.parse_bsdsyscalls(bsd_file)
        mach_syscalls = None
        new_profile = SyscallProfile(bsd_syscalls, mach_syscalls)
        return new_profile
        
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
