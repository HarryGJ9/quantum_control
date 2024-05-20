"""
Script calculates the temporal gradient of the most recently updated genome using the central difference method.

Input: genome updated via gradient ascent of coupling parameters.

Returns: temporal gradient of genome.
"""

import os
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

# Obtain fidelity at specified time, one backwards timestep and one forwards timestep
def fidelity_time_diff(fidelities, specified_time):
    
    # Find index where time matches the specified time
    index = np.where(fidelities[:,0] == specified_time)[0]

    if len(index) > 0:
        # Get the fidelity corresponding to the specific time
        fidelity = fidelities[index[0], 1]
        print("\nFidelity at time {}: {}".format(specified_time, fidelity))
    else:
        print("\nSpecific time {} not found in the array.".format(specified_time))


    return fidelity










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
print(fidelities)
# print(type(fidelities[0,0]))

print(fidelity_time_diff(fidelities, 2.0))




            




