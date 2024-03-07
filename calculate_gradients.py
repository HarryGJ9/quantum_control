# This script takes the fidelities of the adjusted genomes as an input
# And outputs the gradient of the fidelity w.r.t the couplings

import os
import datetime


# Obtain fidelities of adjusted genomes

# Obtain the data_formatted.txt files from each recently generated output- folder
def output_folders():

    # Specify spinchain directory path
    spinchain_path = r'/home/hgjones9/spinchain'

    # Get list of output directories in the spinchain directory
    dirs = os.listdir(spinchain_path)
    print(dirs)

    # Specify the current time to match filtering to output directories
    current_time = datetime.datetime.now()
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    min = current_time.minute

    # Initialise empty list of output- directories
    output_dirs = []

    # Filter the directories to find the relevant outputs
    for dir in dirs:
        if dir.startswith(f'output-{year}-{month}-{day}-{hour}-{min}') and os.path.isdir(dir):
            output_dirs.append(dir)
    print(output_dirs)

    # Sort the output directories by time
    sorted_output_dirs = sorted(output_dirs, lambda x: os.path.getmtime(x))

    return sorted_output_dirs







