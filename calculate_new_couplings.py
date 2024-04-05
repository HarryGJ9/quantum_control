import os
import numpy as np
import time
import datetime
import ast
# from genome_adjuster import couplings

########################
# OPEN GRADIENT.TXT FILE
########################

# # Specify spinchain path
# spinchain_path = r'/home/hgjones9/spinchain'

# Test spinchain path
spinchain_path = 'C:\\Users\harry\quantum_control\outputs_practice'

# List folders under spinchain_path
dirs = os.listdir(spinchain_path)
print(dirs)

# COMMENT OUT UNTIL USED IN UBUNTU SINCE USING A PRACTICE DIRECTORY (CREATED PREVIOUSLY)
# # Look for most recent gradient output.txt file
# for file in dirs:
#     file_creation_time = os.path.getctime(file)
#     if time.time() - file_creation_time <= 60:
#         gradient_output = file
# print(gradient_output)

# Specify gradient output file from practice directory
gradient_output = os.path.join(spinchain_path, 'gradient-2024-3-13-16-37-22.txt') 
print(gradient_output)


# Open gradient.txt file and output the data as a list
with open(gradient_output, 'r') as file:
    gradient_output = file.read()

# Convert data from the .txt file into an array
gradient_lst = ast.literal_eval(gradient_output) # Convert the data from a string to a list
gradient_arr = np.array(gradient_lst) # Convert list to an array
print(gradient_arr)


# Retrieve optimised couplings (PRACTICE)
optimised_couplings = ['349', '349']
optimised_couplings_arr = np.array([int(coupling) for coupling in optimised_couplings])
print(optimised_couplings_arr)

# # Retrive optimised couplings from genome_adjuster.py (REAL)
# optimised_couplings = couplings 
# optimised_couplings_arr = np.array(optimised_couplings)

# Calculate new couplings using gradient ascent
stepsize = 100000 # Arbitrary stepsize
new_couplings_arr = optimised_couplings_arr + stepsize * gradient_arr

# Convert new couplings to integers
new_couplings_arr = [int(coupling) for coupling in new_couplings_arr]
print(new_couplings_arr)


















