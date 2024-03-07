# This script takes the fidelities of the adjusted genomes as an input
# And outputs the gradient of the fidelity w.r.t the couplings

import os
import datetime
import numpy as np


# Obtain fidelities of adjusted genomes

# Obtain the data_formatted.txt files from each recently generated output- folders

# Specify spinchain directory path
spinchain_path = r'/home/hgjones9/spinchain'

# Get list of output directories in the spinchain directory
# dirs = os.listdir(spinchain_path)
# print(dirs)

def list_output_folders(path):
    dirs = os.listdir(path)
    return dirs


# Specify the current time to match filtering to output directories

current_time = datetime.datetime.now()
year = current_time.year
month = current_time.month
day = current_time.day
hour = current_time.hour
min = current_time.minute

def current_time():
    
    current_time = datetime.datetime.now()
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    min = current_time.minute

    return year, month, day, hour, min

# Write function for that returns fidelities of adjusted genomes.

# Initialise empty list of output- directories
output_dirs = []

# Filter the directories to find the relevant outputs
for dir in dirs:
    if dir.startswith(f'output-{year}-{month}-{day}-{hour}-{min}') and os.path.isdir(dir):
        output_dirs.append(dir)
print(output_dirs)

# Sort the output directories by time
sorted_output_dirs = sorted(output_dirs, key=lambda x: os.path.getmtime(x))
print(sorted_output_dirs)

# # SPECIFY PATH FOR PRACTICE FILES
# spinchain_path = "C:\\Users\harry\quantum_control\outputs_practice"
# output_dirs = os.listdir(spinchain_path)
# print(output_dirs)

# Go into each folder -> open 'data' folder -> open 'data_formatted.data' -> save fidelity data in a numpy array
fidelities = [] # Initialise an empty list to store lists of fidelity values for each file
for output_dir in output_dirs:   # Iterate over each output- folder
    path = os.path.join(spinchain_path, output_dir, "data")     # Specify the path to the 'data' folder
    data_sets = os.listdir(path) # List each file in the 'data' folder
    for data_set in data_sets:   # Iterate over each file in the 'data' folder
        if data_set == "dynamics_formatted.data": # If the file is 'data_formatted.data' i.e. contains the fidelities
            with open(os.path.join(path, data_set), 'r') as file: # Open the data_formatted.data file
                next(file) # Skip the first line (title)
                fidelity_values = [] # Initialise an empty list to store fidelity values in
                for line in file: # Iterate over each line
                    values = line.split() # Split each line
                    if values: # If there are values on the line i.e. the line isn't emtpy
                        fidelity_value = complex(values[2]) # Convert into complex number
                        fidelity_values.append(np.linalg.norm(fidelity_value)) # Append to the fidelity_values list with the norm of the fidelity number
            fidelities.append(fidelity_values) # Append the fidelity_values list to the list of fidelities

# print(fidelities)

# Convert the fidelities list of lists into an array
fidelities_array = np.array(fidelities)
# print(fidelities_array)
# print(fidelities_array.shape)

# Transpose the array to ensure that # columnns = # data sets
fidelities_array = fidelities_array.T
# print(fidelities_array)
# print(fidelities_array.shape)

# Number of timesteps 
num_time_steps = len(fidelities_array[:, 0])
# print(num_time_steps)












