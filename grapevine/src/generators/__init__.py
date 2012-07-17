def _import_package_files():
    """ dynamically import all the public attributes of the python modules in
        this file's sub directory
    """
    import os
    import sys
    import traceback

    package_path = os.path.split(__file__)[0]
    package_directory = os.path.split(package_path)[1]

    for fn in os.listdir(package_directory):
        globals_, locals_ = globals(), locals()
        # process all python files in directory that don't start with underscore
        if fn[0] != '_' and fn.split('.')[-1] in ('py', 'pyw'):
            modulename = fn.split('.')[0] # filename without extension
            subpackage = ".".join([package_directory, modulename])
            try:
               module = __import__(subpackage, globals_, locals_, [modulename])
            except:
                traceback.print_exc(file=sys.stdout)
                raise # reraise exception
            for attr_name in dir(module):
                if attr_name[0] != '_':  # public name?
                    globals_[attr_name] = module.__dict__[attr_name]

_import_package_files()
