from datetime import datetime
from .utils import * 

def create_job_folder():
    """Creates a job folder in the default data directory"""
    jobfolder = Path(preferences['data_folder']) / f'job_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    jobfolder.mkdir(parents=True)
    print(f'Job folder created at {jobfolder}')
    return jobfolder 