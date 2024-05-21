"""
Script calculates the temporal gradient of the most recently updated genome using the central difference method.

Input: genome updated via gradient ascent of coupling parameters.

Returns: temporal gradient of genome.
"""

import os
import sys
import numpy as np

# Find time gradient

# Obtain list of fidelities for new genome

# Find fidelity at specified time, one backwards timestep and one forwards time step

# Calculate central difference between a forward and backward timestep



# List directories under specified path
def list_dirs(path):
    dirs = os.listdir(path)
    return dirs

# Open data_formatted for the output_latest file and obtain array of time and fidelities
def get_fidelities(output_dirs):

    fidelities = []
    
    for dir in output_dirs:

        if dir.startswith('output-latest') and os.path.isdir(dir):

            # Specify data paths
            dynamics_data_path = os.path.join(quant_cont_path, dir, 'data', 'dynamics_formatted.data')
            spinchain_out_path = os.path.join(quant_cont_path, dir, 'spinchain.out') 
        
    
           # Load text from dynamics_formatted.data file
            fidelity = np.loadtxt(dynamics_data_path, dtype=complex, comments='#')
            
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

# Obtain fidelity at specified time, one backwards timestep and one forwards timestep and order them in a list
def fidelity_time_diff(fidelities, specified_time):
    
    # Find index where time matches the specified time
    index = np.where(np.isclose(fidelities[:, 0].astype(float), specified_time))[0]

    if index.size > 0:

        # Index of specified time
        idx = index[0]
        
        # Obtain fidelity at specified time and at indices either side
        fidelity = fidelities[idx, 1]
        fidelity_back = fidelities[idx - 1, 1] if (idx - 1) >= 0 else None
        fidelity_forward = fidelities[idx + 1 , 1] if (idx + 1) < fidelities.shape[0] else None

        # Input fidelities into a list 
        fidelity_lst = [fidelity_back, fidelity, fidelity_forward]
        fidelity_lst = [round(fidelity * 100, 2) for fidelity in fidelity_lst]

        # Input times into a list
        time_lst = [fidelities[idx - 1,0], fidelities[idx,0], fidelities[idx + 1,0]]
        time_lst = [float(round(time, 2)) for time in time_lst]

        # Stack lists together into an array
        time_fidelity_arr = np.column_stack((time_lst, fidelity_lst))

    else:
        print(f"The value {specified_time} is not found in the array.")

    return time_fidelity_arr

def max_fidelity_time(time_fidelity_arr):

    # Find index of maximum value
    max_index = np.argmax(time_fidelity_arr[:,1])

    # Obtain row corresponding to that index
    max_vals = time_fidelity_arr[max_index]

    return max_vals


###############
# RUN PROGRAMME 
###############

# Specify quantum_control_path
quant_cont_path = r'/home/hgjones9/quantum_control'

# Obtain all directories under quantum_control
output_dirs = list_dirs(quant_cont_path)
# print(output_dirs)

# Obtain fidelity against time values
fidelities = get_fidelities(output_dirs)
# print(fidelities)

# Retrieve specified time at initial max fidelity for input to fidelity_time_diff
specified_time = float(sys.argv[1])
# specified_time = 2.0

# Obtain 2D array of forwards and backwards time and fidelity values
time_fidelity_arr = fidelity_time_diff(fidelities, specified_time)
# print(time_fidelity_arr)

# Pick highest value of fidelity and specify new corresponding time
max_vals = max_fidelity_time(time_fidelity_arr)
# print(max_vals)

# Save new fidelity
new_fidelity = max_vals[1]

# Write new fidelity to .txt file
with open('/home/hgjones9/quantum_control/new_fidelity.txt', 'w') as file:
    file.write(str(new_fidelity))

# Save new time
new_time = max_vals[0]

# Write updated time to a file
with open('/home/hgjones9/quantum_control/new_time.txt', 'w') as file:
    file.write(str(new_time))





            




