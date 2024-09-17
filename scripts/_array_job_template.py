import sys
import numpy as np
from pathlib import Path
from pybatch import parse_cli_args, load_subjob_params

'''
This is a template for an array job. 
The way Univa Grid Engine is set up, we get the sub job number from the command line
statement that was used to run this script. The sub-job number will be the first
positional argument returned from parse_cli_args().
'''

def fit_model(alpha, tol, solver):
    ############
    # MODIFY THIS CELL OF CODE TO WHATEVER YOU NEED TO RUN IN PARALLEL
    from sklearn.datasets import load_diabetes
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import cross_val_score
    # load toy data
    dat = load_diabetes()

    # fit model
    mdl = Ridge(alpha=alpha, tol=tol, solver=solver)
    scores = cross_val_score(mdl, dat.data, dat.target, cv=5)
    print(f'Scores for alpha={alpha}, tol={tol}, solver={solver}: {scores}')
    return scores
    #############

if __name__ == '__main__':
    job_index, args, kwargs = parse_cli_args(get_job_index=True)
    params = load_subjob_params(kwargs['params_file'], job_index)
    scores = fit_model(**params)
    savename = Path(kwargs['output_savepath']) / f'output_{job_index}.npy'
    print(f'Saving scores to {savename}')
    np.save(savename, scores) # save outputs to the proper folder 