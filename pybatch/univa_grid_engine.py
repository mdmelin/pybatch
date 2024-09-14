import subprocess as sub
from .utils import * 
from .parse import *
import numpy as np

ARRAY_SUBMISSION_TEMPLATE = """
#!/bin/bash
mkdir -p {savepath}

#$ -cwd
# error = Merged with joblog
#$ -o {logname}.$JOB_ID.$TASK_ID

#$ -j y
#$ -l h_rt=24:00:00,h_data=4G
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
echo "{pyfile} "$SGE_TASK_ID" {pyfile_args} {pyfile_kwargs}"

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

def create_job_array_script(savepath, 
                            pyfile,
                            n_subjobs,
                            n_cpu_per_job=3,
                            modules=['anaconda3'],
                            conda_env='max_glmhmm',
                            pyfile_args=None,
                            pyfile_kwargs=None): #pyfile is the absolute path of the python file to be run
    savepath = Path(savepath)
    logname = savepath / 'logs' / 'joblog'
    output_savepath = savepath / 'output'
    filename = savepath / 'submission_script.sh'
    # args should be a list of args that will be passed to the python file we wish to run
    if filename.exists():
        raise FileExistsError("Submission script already exists")
    
    pyfile_kwargs = dict(params_file=savepath / 'params.npy',
                         output_savepath=output_savepath,)
                         
    
    submission_text = ARRAY_SUBMISSION_TEMPLATE.format(savepath=savepath,
                                                       logname=logname,
                                                       n_subjobs=n_subjobs,
                                                       pyfile=pyfile,
                                                       n_cpu_per_job=n_cpu_per_job,
                                                       conda_env=conda_env,
                                                       modules=list_to_cmd_args_string(modules),
                                                       pyfile_args=list_to_cmd_args_string(pyfile_args),
                                                       pyfile_kwargs=dict_to_cmd_args_string(pyfile_kwargs),)

    with open(filename,'w') as file:
        file.writelines(submission_text)
    print(f'Submission script created at {filename}')
    return filename



def submit_job():
    return
    