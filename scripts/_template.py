from pybatch import parse_cli_args
import sys
'''
This is a template for a script that uses the parse_cli_args function from pybatch/parse.py
to parse command line arguments and pass them to a function. Allowing you to run any python function
with full argument control from the command line.
'''

def myfunc(arg_a, arg_b=None, arg_c=None):
    # do stuff with args here
    return

if __name__ == '__main__':
    args, kwargs = parse_cli_args() # collects positional and keyword arguments from the command line
    print(args)
    print(kwargs)
    myfunc(*args, **kwargs)