"""
Script calculates the gradient of fidelity w.r.t couplings through the central difference method.

Input: Fidelities of adjusted genomes

Returns: Gradient of fidelity w.r.t couplings
"""

import os
import datetime
import time
import numpy as np
import re
import ast
import sys


# Specify quantum_control directory path
quant_cont_path = r'/home/hgjones9/quantum_control'

# # SPECIFY PATH FOR PRACTICE FILES
# spinchain_path = "C:\\Users\harry\quantum_control\outputs_practice"
# output_dirs = os.listdir(spinchain_path)
# print(output_dirs)

# List all folders under a specific path
def list_dirs(path):
    dirs = os.listdir(path)
    return dirs


# Filter through the folders under spinchain and find those most recently created 
def filter(dirs, N):

    # Filter directories that start with 'output-' and are genuine directories
    filtered_dirs = [dir for dir in dirs if dir.startswith('output-') and os.path.isdir(dir)]

    # Sort directories by creation time in descending order
    sorted_dirs = sorted(filtered_dirs, key=lambda dir: os.path.getctime(dir), reverse=True)

    # Exclude 'output-latest' directory if present
    sorted_dirs = [dir for dir in sorted_dirs if dir != 'output-latest']

    # Take the first N directories, where N = no. of adjusted couplings = 2 x no. of couplings
    output_dirs = sorted_dirs[:N]

    # Flip the list 
    output_dirs.reverse()

    return output_dirs

# Function which returns a 2D array of time and fidelity values for a set of output folders
def fidelities(output_dirs):
    
    # Initialise fidelity list
    fidelities = [] 

    timesteps = None

    # Iterate over the output- directories and obtain fidelity values
    for output_dir in output_dirs:

        # Specify relevant paths
        data_path = os.path.join(quant_cont_path, output_dir, "data")
        spinchain_out_path = os.path.join(quant_cont_path, output_dir, "spinchain.out") 
        
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

    # print(fidelity_time_arr)

    return fidelity_time_arr

# Function which returns the fidelities of each adjusted genome at the specified time
def fidelities_at_time(fidelity_time_arr):

    # # Open max_fidelity_time.txt to get the specified time
    # with open('/home/hgjones9/quantum_control/max_fidelity_time.txt') as file:
    #     lines = file.readlines()
    #     if len(lines) >= 2:
    #         specified_time = lines[1].strip()
    #         # print(specified_time)

    # Specify time to find fidelities
    specified_time = round(float(sys.argv[1]), 2)

    # Format fidelity_time_arr such that the time column are all of the form e.g. '2.40' not '2.40000000e+00'
    formatted_times = [round(float(time), 2) for time in fidelity_time_arr[:,0]]
   
    # Check if the specified time exists in the array
    if specified_time in formatted_times:

        # Find the index of the specified time
        row_index = formatted_times.index(specified_time)

        # Extract fidelities at the specified time
        fidelities_at_time_arr = fidelity_time_arr[row_index, 1:]
        # print(f"Fidelities at time {specified_time} : {fidelities_at_time_arr}")

    else:
        print("Specified time not found in the array")

    return fidelities_at_time_arr

# Function which calculates the gradient through central difference of each pair of fidelities
def calculate_gradient(fidelities, couplings, h=0.1):


    # Ensure the input lists are of correct lengths
    if len(fidelities) != 2 * len(couplings):
        raise ValueError("The length of fidelities should be twice the length of couplings")

    gradient_lst = []

    # Iterate over each coupling and corresponding pair of fidelities
    for i in range(len(couplings)):
        f_plus = fidelities[2 * i]
        f_minus = fidelities[2 * i + 1]
        coupling = couplings[i]
        central_diff = (f_plus - f_minus) / (2 * h * coupling)
        gradient_lst.append(central_diff)

    # # Convert list to numpy array
    # gradient_arr = np.array(gradient)

    return gradient_lst



###############
# RUN PROGRAMME 
###############

# Specify quantum_control directory path
quant_cont_path = r'/home/hgjones9/quantum_control'

# Obtain all output- directories under quantum_control
dirs = list_dirs(quant_cont_path)
# print(dirs)

# Obtain number of adjusted couplings

# Specify path to the updated genome
genome_path = os.path.join(quant_cont_path, 'old_couplings.txt')

# Open file old_couplings.txt and count couplings
with open(genome_path, 'r') as file:
    couplings_str = file.read()

# Convert string into list
couplings_lst = ast.literal_eval(couplings_str)

# Count couplings
num_couplings = len(couplings_lst)

# Specify N = how many recent files to use = how many adjusted couplings there are
N = 2 * num_couplings

# Call filter function to get the relevant output- directories, filtered by time
sorted_output_dirs = filter(dirs, N)
# print(f"Sorted output directories: {sorted_output_dirs}")

# Call fidelities function to get an array of updated fidelities
updated_fidelities = fidelities(sorted_output_dirs)
# print(f"Fidelities of adjusted genomes: {updated_fidelities}")
# print((updated_fidelities[:,0] - updated_fidelities[:,1]) / (2))

# Obtain fidelities at the time of max fidelity provided by the initial genome.out file
fidelity_vals = fidelities_at_time(updated_fidelities)
fidelity_vals = fidelity_vals * 100
# print(f'Fidelity values at specified time: {fidelity_vals}')

# Call calculate_gradient to obtain the gradient vector
gradient = calculate_gradient(fidelity_vals, couplings_lst)
# print(f"Gradient vector: {gradient}")

with open('/home/hgjones9/quantum_control/gradient_latest.txt', 'w') as file:
    file.write(str(gradient))










