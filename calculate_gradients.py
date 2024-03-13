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
            if time.time() - dir_creation_time <= 60: # Obtain all directories created in the last two minutes
                output_dirs.append(dir)
    # print(output_dirs)
                
    # Remove 'output-latest' directory
    output_dirs.remove('output-latest')
    # print(output_dirs)

    # Sort the output directories by time
    sorted_output_dirs = output_dirs.sort(reverse=False, key=lambda x: os.path.getmtime(x))
    # print(sorted_output_dirs)

    return sorted_output_dirs

# Function which returns a 2D array of fidelity values for a set of output folders
def fidelities(output_dirs):
    
    # Initialise fidelity list
    fidelities = [] 

    timesteps = None

    # Iterate over the output- directories and obtain fidelity values
    for output_dir in output_dirs:

        # Specify relevant paths
        data_path = os.path.join(spinchain_path, output_dir, "data")
        spinchain_out_path = os.path.join(spinchain_path, output_dir, "spinchain.out") 
        
        # List data_sets in output-folder
        data_sets = os.listdir(data_path)

        for data_set in data_sets:
            if data_set == 'dynamics_formatted.data':
                
                # Load text from dynamics_formatted.data file
                fidelity = np.loadtxt(os.path.join(data_path, 'dynamics_formatted.data'), dtype=complex, comments='#')

                # Obtain timesteps from dynamics_formatted.data file
                timesteps = np.absolute(fidelity[:,0])

                # TAKEN FROM DYNAMICS.PY
                # Obtains an array of fidelities for each output- file
                init = fidelity[:, 1]*0.0
                final = fidelity[:, 1]*0.0
                numI = 0
                numF = 0
                initialIndexes = []
                initialCoeffs = []
                finalIndexes = []
                finalCoeffs = []
                inInit = True

                with open(spinchain_out_path, "r") as f:
                    for line in f:
                        if "FINAL VECTOR" in line:
                            inInit = False
                            split = line.split()
                            # final += fidelity[:, int(split[4])]
                            finalIndexes.append(int(split[4]))
                            numF += 1
                        elif "INITIAL INJECTED" in line:
                            split = line.split()
                            # init += fidelity[:, int(split[5])]
                            initialIndexes.append(int(split[5]))
                            numI += 1
                        elif "WITH COEFFICIENT" in line:
                            split = line.split()
                            realVal = float(split[4][:-1])
                            imagVal = float(split[5][:-1])
                            if inInit:
                                initialCoeffs.append(complex(realVal, imagVal))
                            else:
                                finalCoeffs.append(complex(realVal, imagVal))
                        elif "FOR MODE 2" in line:
                            break

                # Construct the vectors
                for i in range(numI):
                    init = init + np.conj(initialCoeffs[i]) * fidelity[:, initialIndexes[i]]
                for i in range(numF):
                    final = final + np.conj(finalCoeffs[i]) * fidelity[:, finalIndexes[i]]

                #PLOT FIDELITY AGAINST INITIAL STATE AND TARGET STATE (CHANGE WHENEVER)
                y1 = (np.absolute(init))**2
                y2 = (np.absolute(final))**2

                fidelities.append(y2)
                if timesteps is None:
                    timesteps = fidelity[:,0]
    
    # Convert list of arrays to a 2D array with # rows = # timesteps and fidelities in the columns
    fidelities_arr = np.stack(fidelities, axis=1)
    # print(fidelities_arr)

    # Stack time and fidelity arrays together
    fidelity_time_arr = np.hstack((timesteps.reshape(-1, 1), fidelities_arr))

    return fidelity_time_arr


# # Function to calculate the NxM matrix of central differences 
# # N = number of timesteps
# # M = central differences 
# def calculate_gradient(fidelities, h=1):

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

# Function which returns the maximum fidelity and corresponding time for each column of fidelities
def max_fidelity(fidelities):

    # print(fidelities.shape)

    # Array of timesteps
    time_arr = fidelities[:,0]
    # print(time_arr)

    # Obtain fidelity values by first column (timesteps) 
    fidelity_vals = fidelities[:,1:]
    # print(fidelity_vals)

    # Maximum fidelities of each row 
    max_fidelities = np.amax(fidelity_vals, axis=0)
    # print(max_fidelities)

    # Find corresponding time index at which max fidelity occurs
    max_indices = np.argmax(fidelity_vals, axis=0)
    # print(max_indices)

    # # Find time value at which max fidelity index occurs
    time = time_arr[max_indices]
    # print(time)

    return max_fidelities, time

# Function which calculates the gradient through central difference of each pair of fidelities
def calculate_gradient(fidelities, h=1):

    # Obtain number of columns
    num_columns = len(fidelities)

    # Iterate over each column pair and find the central difference, then append it to gradient list
    gradient = []
    for i in range(0, num_columns-1,2):
        central_diff = ((fidelities[i] - h) - (fidelities[i + 1] - 1)) / (2 * h)
        gradient.append(central_diff)

    # Convert list to numpy array
    gradient_arr = np.array(gradient)

    return gradient


# Call list_dirs to obtain all output- directories under spinchain
dirs = list_dirs(spinchain_path)
print(dirs)

# Call filter function to get the relevant output- directories, filtered by time
sorted_output_dirs = filter(dirs)
print(sorted_output_dirs)

# # Call fidelities function to get an array of updated fidelities
# updated_fidelities = fidelities(sorted_output_dirs)
# # print(updated_fidelities)
# # print((updated_fidelities[:,0] - updated_fidelities[:,1]) / (2))

# # Obtain max fidelities from each column (exclude time column)
# max_fidelities, max_times = max_fidelity(updated_fidelities)
# # print(max_fidelities)
# # print(max_times)

# # # Call calculate_gradient to obtain the gradient vector
# gradient = calculate_gradient(max_fidelities)
# # print(gradient)

# # Retrieve current times
# year = current_time()[0]
# month = current_time()[1]
# day = current_time()[2]
# hour = current_time()[3]
# min = current_time()[4]
# sec = current_time()[5]

# # Write the gradient vector out to a .txt file
# with open(f'/home/hgjones9/spinchain/gradient-{year}-{month}-{day}-{hour}-{min}-{sec}.txt', 'w') as file:
#     file.write(str(gradient))










