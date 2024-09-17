import shlex 
import argparse
import sys
import ast
from .utils import *

"""
A module that you will use in your own python scripts. It helps with taking
command line arguments (which are delivered with the batch submission script)
and passing them as arguments to your python functions.
"""

def dict_to_cmd_args_string(d):
    if d is None:
        return ''
    args = []
    for key, value in d.items():
        # Convert the key to a command-line argument (e.g., "--key")
        if isinstance(value, list):  # Handle list values
            args.append(f"--{key}")
            for v in value:
                args.append(str(v))
        else:
            args.append(f"--{key}")
            args.append(str(value))
    return ' '.join(args)

def list_to_cmd_args_string(l):
    if l is None:
        return ''
    return ' '.join(str(x) for x in l)

def parse_cli_args(cli_args=None, get_job_index=False):
    #input = shlex.split(sys.argv)
    if cli_args is None:
        cli_args = sys.argv[1:] # drop the python filepath
    parser = argparse.ArgumentParser()
    # construct the parser appropriately
    i = 0
    kwarg_indices = np.where([i.startswith('--') for i in cli_args])[0]
    while i < len(cli_args):
        if cli_args[i].startswith('--'):
            next_arg_index = kwarg_indices[kwarg_indices>i]
            if len(next_arg_index)==0:
                next_arg_index = len(cli_args) # handle termination of the input
                nargs = len(cli_args)-i-1
            else:
                next_arg_index = next_arg_index[0]
                nargs = next_arg_index-i-1
            parser.add_argument(cli_args[i], dest=cli_args[i].replace('--',''), nargs=nargs)
            i=next_arg_index
        else:
            parser.add_argument(cli_args[i])
            i+=1
    args = parser.parse_args(cli_args)
    typed_kwargs = dict()
    typed_args = []
    for key, val in vars(args).items():
        if key == val:
           typed_args.append(infer_type_from_string(val)) 
           continue
        if len(val)==1:
            typed_kwargs[key] = infer_type_from_string(val[0])
        else:
            typed_kwargs[key] = [infer_type_from_string(v) for v in val]
    if get_job_index:
        job_index = typed_args[0] - 1 # job index is always the first positional arg. UGE uses 1-based indexing
        return job_index, typed_args[1:], typed_kwargs
    else:
        return typed_args, typed_kwargs

def infer_type_from_string(value):
    value = value.strip()  # Remove leading/trailing whitespace

    # Try to convert to int
    if value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
        return int(value)

    # Try to convert to float
    try:
        return float(value)
    except ValueError:
        pass

    # Try to convert to boolean
    if value.lower() in ("true", "false"):
        return value.lower() == "true"

    # Try to convert to list or dictionary
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        pass

    # Return the original string if no other conversion is successful
    return value

    