from .utils import * 
from .io import create_job_folder
import numpy as np
import itertools

def create_params_array_grid(params_dict,
                             savepath=None,
                             overwrite=False,
                             save=True,):
    """
    Creates a basic grid from the supplied parameters
    """
    if savepath is not None:
        savepath = Path(savepath)
    else:
        savepath = create_job_folder()
    paramspath = savepath / 'params.npy'
    paramsnamespath = savepath / 'params_names.npy'
    if paramspath.exists() and not overwrite:
        print("Params file already exist in this folder. Skipping creation and loading it.")
        param_matrix = np.load(paramspath, allow_pickle=True)
        param_names = np.load(paramsnamespath, allow_pickle=True)
        return param_matrix, param_names
    

    param_names = list(params_dict.keys())
    param_vals = list(params_dict.values())
    params_matrix = np.array(list(itertools.product(*param_vals)), dtype=object)
    
    if not save:
        return params_matrix 

    if not savepath.exists():
        savepath.mkdir(parents=True)
    with open(paramspath, 'wb') as f:
        np.save(f, params_matrix)
    with open(paramsnamespath, 'wb') as f:
        np.save(f, param_names)
    #jobnumfile = savepath / 'jobnum.npy'
    #with open(jobnumfile, 'wb') as f:
    #    np.save(f, numruns)
    return params_matrix, param_names

def load_subjob_params(params_path, job_index):
    """
    Loads the parameters for a subjob
    """
    params = np.load(params_path, allow_pickle=True)
    param_names = np.load(params_path.parent / 'params_names.npy', allow_pickle=True)
    params_dict = dict(zip(param_names, params[job_index]))
    return params_dict
