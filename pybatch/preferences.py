import json 
from pathlib import Path
# Default preferences
DEFAULT_DATA_DIR = Path().home() / 'pybatch' / 'jobs'
PREFS_FILE = Path().home() / 'pybatch' / 'preferences.json'
DEFAULT_PREFS = dict(data_folder=str(DEFAULT_DATA_DIR),)

# TODO: add default number of cpus, memory, etc. to preferences file

def __setup_prefs():
    if not DEFAULT_DATA_DIR.exists():
        print(f'Creating directory {DEFAULT_DATA_DIR}')
        DEFAULT_DATA_DIR.mkdir(parents=True)
    print(DEFAULT_PREFS)
    with open(PREFS_FILE,'w') as fd:
        json.dump(DEFAULT_PREFS,
                  fd,
                  sort_keys=True,
                  indent=4)
    print(f'Preferences file created at {PREFS_FILE}')

def __load_prefs():
    with open(PREFS_FILE,'r') as fd:
        prefs = json.load(fd)
    for k in DEFAULT_PREFS:
        if k not in prefs.keys():
            prefs[k] = DEFAULT_PREFS[k]
    return prefs

# Preferences

if not PREFS_FILE.exists():
    __setup_prefs()

preferences = __load_prefs()