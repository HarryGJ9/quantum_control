"""
Retrieve fidelity from 3 most recent spinnet calls for use in the temporal gradient.

Then see which timing 
"""
import os
import datetime
import time
import numpy as np
import re

# List all folders under a specific path
def list_dirs(path):
    dirs = os.listdir(path)
    return dirs

# Filter through the folders under spinchain and find those most recently created 
def filter(dirs):

    # Filter directories that start with 'output-' and are genuine directories
    filtered_dirs = [dir for dir in dirs if dir.startswith('output-') and os.path.isdir(dir)]

    # Sort directories by creation time in descending order
    sorted_dirs = sorted(filtered_dirs, key=lambda dir: os.path.getctime(dir), reverse=True)

    # Exclude 'output-latest' directory if present
    sorted_dirs = [dir for dir in sorted_dirs if dir != 'output-latest']

    # Take the first 3 directories
    output_dirs = sorted_dirs[:2]

    # Flip the list 
    output_dirs.reverse()

    return output_dirs

# Look through the filtered directories to obtain fidelities at a time increment before, after and at the specified time
def fidelity_time(output_dirs):

    # Initialise fidelity and time lists
    fidelities = []
    times = []

    # For each output directory, open 'genetic.out' and extract the fidelity value at the specified time
    for dir in output_dirs:
        with open(os.path.join(dir, 'genetic.out'), 'r') as file:
            for line in file:
                if line.startswith('with fitness'):
                    fidelity_match = re.search(r'(\d+\.\d+)% fidelity', line)
                    time_match = re.search(r'at time (\d+\.\d+)', line)
                    if fidelity_match:
                        fidelity = fidelity_match.group(1)
                        time = time_match.group(1)
        fidelities.append(fidelity)
        times.append(time)

    return fidelities, times

# Stack the fideltiy and time lists together and pick out the row with the highest fidelity
def stack(fidelity_vals, time_vals):

    # Convert both lists into arrays
    fidelity_arr = np.array(fidelity_vals)
    time_arr = np.array(time_vals)

    # Stack so that column 0 = time and column 1 = fidelities
    fidelity_time_arr = np.column_stack((time_arr, fidelity_arr))

    # Find index of maximum value
    max_index = np.argmax(fidelity_time_arr[:,1])

    # Obtain row corresponding to that index
    max_vals = fidelity_time_arr[max_index]

    return max_vals


###############
# Run programme
###############

path = '/home/hgjones9/quantum_control'

# Get output directories for quantum_control
dirs = list_dirs(path)

# Filter to get 3 most recent directories i.e. those containing fidelity calculations at 3 separate times
output_dirs = filter(dirs)

# Obtain fidelities and times for each timing increment and output as two separate lists
fidelity_vals, time_vals = fidelity_time(output_dirs)

# Obtain maximum fidelity and corresponding time
max_fidelity_time = stack(fidelity_vals, time_vals)

# Save new fidelity
new_fidelity = max_fidelity_time[1]

# Write new fidelity to .txt file
with open('/home/hgjones9/quantum_control/new_fidelity.txt', 'w') as file:
    file.write(str(new_fidelity))

# Save new time
new_time = max_fidelity_time[0]

# Write updated time to a file
with open('/home/hgjones9/quantum_control/new_time.txt', 'w') as file:
    file.write(str(new_time))


