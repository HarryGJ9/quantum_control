# This script takes the fidelities of the adjusted genomes as an input
# And outputs the gradient of the fidelity w.r.t the couplings

import os
import datetime
import time
import numpy as np

# Specify spinchain directory path
spinchain_path = r'/home/hgjones9/spinchain'

# # SPECIFY PATH FOR PRACTICE FILES
# spinchain_path = "C:\\Users\harry\quantum_control\outputs_practice"
# output_dirs = os.listdir(spinchain_path)
# print(output_dirs)

# List all folders under a specific path
def list_dirs(path):
    dirs = os.listdir(path)
    return dirs

# Function which obtains current time, used to filter through folders in spinchain
def current_time():
    
    current_time = datetime.datetime.now()
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    min = current_time.minute
    sec = current_time.second

    return year, month, day, hour, min, sec

# Function which filters through the folders under spinchain and finds those most recently created 
def filter(dirs):

    # # Obtain current times
    # year = current_time()[0]
    # month = current_time()[1]
    # day = current_time()[2]
    # hour = current_time()[3]
    # min = current_time()[4]

    # Initialise empty list of output directories
    output_dirs = []

    # Iterate over the folders and add the most recent ones to a list of output- directories
    for dir in dirs:
        if dir.startswith('output-') and os.path.isdir(dir): 
            dir_creation_time = os.path.getctime(dir)
            if time.time() - dir_creation_time <= 120: # Obtain all directories created in the last two minutes
                output_dirs.append(dir)
    # print(output_dirs)
                
    # Remove 'output-latest' directory
    output_dirs.remove('output-latest')

    # Sort the output directories by time
    sorted_output_dirs = output_dirs.sort(reverse=False, key=lambda x: os.path.getmtime(x))
    print(sorted_output_dirs)

    # return sorted_output_dirs
    return output_dirs

# Function which looks through each output directory and returns an array of fidelities
def fidelities(output_dirs):

    # Go into each folder -> open 'data' folder -> open 'data_formatted.data' -> save fidelity data in a numpy array
    fidelities = [] # Initialise an empty list to store lists of fidelity values for each file
    for output_dir in output_dirs:   # Iterate over each output- folder
        path = os.path.join(spinchain_path, output_dir, "data")   # Specify the path to the 'data' folder
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

    return fidelities_array

# Function to calculate the NxM matrix of central differences 
# N = number of timesteps
# M = central differences 
def calculate_gradient(fidelities, h=1):

    # Obtain number of columns to iterate over
    num_rows, num_columns = fidelities.shape
    print(num_columns)
    # print(num_columns)

    # Initialise gradient vector
    gradient = []

    # Iterate over columns and calculate the central difference for each timestep
    for i in range(0, num_columns-1,2):
        central_diff = (fidelities[:,i] - fidelities[:,i+1]) / (2 * h)
        # print(fidelities[:,i])
        # print(fidelities[:,i+1])
        # print(central_diff)
        gradient.append(central_diff)

    # Convert list of lists into an array
    gradient_array = np.array(gradient).T

    return gradient_array


# Call list_dirs to obtain all output- directories under spinchain
dirs = list_dirs(spinchain_path)
print(dirs)

# Call filter function to get the relevant output- directories, filtered by time
sorted_output_dirs = filter(dirs)
print(sorted_output_dirs)

# Call fidelities function to get an array of updated fidelities
updated_fidelities = fidelities(sorted_output_dirs)
# print(updated_fidelities)
# print((updated_fidelities[:,0] - updated_fidelities[:,1]) / (2))

# # Call calculate_gradient to obtain the gradient vector
gradient = calculate_gradient(updated_fidelities)
# print(gradient)

# # Retrieve current times
# year = current_time()[0]
# month = current_time()[1]
# day = current_time()[2]
# hour = current_time()[3]
# min = current_time()[4]
# sec = current_time()[5]

# Write the gradient vector out to a .txt file
with open(f'/home/hgjones9/spinchain/gradient-{year}-{month}-{day}-{hour}-{min}-{sec}.txt', 'w') as file:
    file.write(str(gradient))









