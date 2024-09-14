import argparse
from .utils import *

def main(command_line=None):
    parser = argparse.ArgumentParser('pybatch')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug info'
    )
    subparsers = parser.add_subparsers(dest='command')

    # submit job subparser
    submit_job_parser = subparsers.add_parser('submit_job', help='Show calibration curve for a device')

    # create job subparser
    create_job_parser = subparsers.add_parser('create_job', help='Create parameters array and submission script for a batch array job')
    #calibrate.add_argument(
    #    '--dry-run',
    #    help='do not write the results to calibration file',
    #    action='store_true',
    #)

    # submit prepared job subparser
    submit_prepared_job_parser = subparsers.add_parser('submit_prepared_job', help='Show calibration curve for a device')


    args = parser.parse_args(command_line)

    # TODO: implement cli logic here
    
    if __name__ == '__main__':
        main()