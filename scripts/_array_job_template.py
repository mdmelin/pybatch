import sys
import numpy as np
from pybatch import parse_cli_args, load_subjob_params

'''
This is a template for an array job. 
The way Univa Grid Engine is set up, we get the sub job number from the command line
statement that was used to run this script. The sub-job number will be the first
positional argument returned from parse_cli_args().
'''

def fit_model(parameter_a, parameter_b, parameter_c):
    # fit model here
    return log_likelihood

if __name__ == '__main__':
    args, kwargs = parse_cli_args()
    job_index = args[0] - 1 # job index is always the first positional arg. UGE uses 1-based indexing
    params = load_subjob_params(kwargs['params_file'], job_index)
    log_likelihood = fit_model(**params)
    savename = kwargs['output_savepath'] / f'output_{job_index}.npy'
    np.save(savename, log_likelihood)