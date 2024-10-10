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
    param_vals = [v if isinstance(v, list) else [v] for v in param_vals] # handle params with a single value
    params_matrix = np.array(list(itertools.product(*param_vals)), dtype=object)
    print(f'Created parameter grid with {params_matrix.shape[0]} parameter sets')
    
    if not save:
        return params_matrix, param_names

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

def assemble_outputs(save_dir, file_prefix='output'):
    save_dir = Path(save_dir)

    npy_files = (save_dir / 'output').glob(f'{file_prefix}*.npy')
    params = np.load(save_dir / 'params.npy', allow_pickle=True)
    n_expected = params.shape[0]
    out = np.empty((n_expected,), dtype=object)
    returned_inds = []
    for file in npy_files:
        i = int(''.join([char for char in file.with_suffix('').name if char.isdigit()])) # get digits from filename
        dat = np.load(file)
        out[i] = dat
        returned_inds.append(i)
    print(f'Expected {n_expected} outputs. Found {len(returned_inds)}.')
    return params, out, returned_inds

def load_params(savepath):
    savepath = Path(savepath)
    params = np.load(savepath / 'params.npy', allow_pickle=True)
    param_names = np.load(savepath / 'params_names.npy', allow_pickle=True)
    params_dict = dict()
    for i, name in enumerate(param_names):
        params_dict[name] = params[:,i]
    return params_dict

def load_subjob_params(params_path, job_index):
    """
    Loads the parameters for a subjob
    """
    params_path = Path(params_path)
    params = np.load(params_path, allow_pickle=True)
    param_names = np.load(params_path.parent / 'params_names.npy', allow_pickle=True)
    params_dict = dict(zip(param_names, params[job_index]))
    return params_dict
