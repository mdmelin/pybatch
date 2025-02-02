import subprocess as sub
from .utils import * 
from .parse import *
from .io import create_job_folder
from datetime import timedelta
from .parameters import create_params_array_grid

# TODO: move this to an engines.py file for different submission engines
ARRAY_SUBMISSION_TEMPLATE = """
#!/bin/bash
mkdir -p {savepath}

#$ -cwd
# error = Merged with joblog
#$ -o {logname}.$JOB_ID.$TASK_ID

#$ -j y
#$ -l h_rt={jobtime},h_vmem={memory_gb}G,{queue_flags_string}
#$ -pe shared {n_cpu_per_job}

#$ -t 1-{n_subjobs}:1

#. /u/local/Modules/default/init/modules.sh
source $HOME/.bash_profile
module load {modules}
conda activate {conda_env}


echo "JOB started on:  " `hostname -s`
echo "JOB started on:  " `date `
echo " "
echo " " # the command goes in quotes   


echo "This is sub-job $SGE_TASK_ID"
echo "python {pyfile} "$SGE_TASK_ID" {pyfile_args} {pyfile_kwargs}"

python {pyfile} "$SGE_TASK_ID" {pyfile_args} {pyfile_kwargs} #run the python script with the proper index

echo "JOB ended on:  " `hostname -s`
echo "JOB ended on:  " `date `
echo " "
"""

def has_queue():
    proc = sub.Popen('qstat', shell=True, stdout=sub.PIPE, stderr = sub.PIPE)
    out,err = proc.communicate()
    if len(err):
            return False
    return True

def create_and_submit_parameter_grid_array(pyfile, params_dict, savepath=None, **kwargs):
    if savepath is not None:
        savepath = Path(savepath)
    else:
        savepath = create_job_folder()
    params, names = create_params_array_grid(params_dict,savepath=savepath)
    submission_script_path = create_job_array_script(savepath, pyfile, len(params), **kwargs)
    submit_job(submission_script_path)
    return params, savepath


# TODO: add a queue option
def create_job_array_script(savepath, 
                            pyfile,
                            n_subjobs,
                            jobtime_hrs=10,
                            n_cpu_per_job=3,
                            memory_gb=4,
                            modules=['anaconda3'],
                            queue_flags=None,
                            conda_env='ssm',
                            pyfile_args=None,
                            pyfile_kwargs=None): #pyfile is the absolute path of the python file to be run
    if not Path(pyfile).exists():
        raise FileNotFoundError('The python file provided does not exist')
    savepath = Path(savepath)
    logname = savepath / 'logs' / 'joblog'
    output_savepath = savepath / 'output'
    output_savepath.mkdir(exist_ok=True)
    filename = savepath / 'submission_script.sh'
    # args should be a list of args that will be passed to the python file we wish to run
    if filename.exists():
        raise FileExistsError("Submission script already exists")
    
    if pyfile_kwargs is None:
        pyfile_kwargs = dict(params_file=savepath / 'params.npy',
                             output_savepath=output_savepath,)
    else:
        temp = dict(params_file=savepath / 'params.npy',
                    output_savepath=output_savepath,)
        pyfile_kwargs = {**pyfile_kwargs, **temp}
    jobtime = timedelta(hours=jobtime_hrs)                      
    jobtime = format_timedelta(jobtime)
    # Note to self: time format follows 24:00:00 
    submission_text = ARRAY_SUBMISSION_TEMPLATE.format(savepath=savepath,
                                                       logname=logname,
                                                       jobtime=jobtime,
                                                       memory_gb=memory_gb,
                                                       n_subjobs=n_subjobs,
                                                       pyfile=str(pyfile),
                                                       n_cpu_per_job=n_cpu_per_job,
                                                       conda_env=conda_env,
                                                       queue_flags_string=list_to_cmd_args_string(queue_flags, delimiter=','),
                                                       modules=list_to_cmd_args_string(modules),
                                                       pyfile_args=list_to_cmd_args_string(pyfile_args),
                                                       pyfile_kwargs=dict_to_cmd_args_string(pyfile_kwargs),)

    with open(filename,'w') as file:
        file.writelines(submission_text)
    print(f'Submission script created at {filename}')
    return filename

def submit_job(submission_script_path):
    import subprocess
    cmd = ['qsub', str(submission_script_path)]
    print(f'Submitting job with command: {cmd}')
    out = subprocess.check_output(cmd)
    print(out)
    return
    