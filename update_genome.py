import os
import numpy as np
import time
import datetime
import ast
import genome_adjuster
# from genome_adjuster import couplings
# from genome_adjuster import genome


##########################
# TEST
##########################

# # Test spinchain path
# spinchain_path = 'C:\\Users\harry\quantum_control\outputs_practice'

# # Specify gradient output file from practice directory
# gradient_output = os.path.join(spinchain_path, 'gradient-2024-3-13-16-37-22.txt') 
# print(gradient_output)

# # Open gradient.txt file and convert the gradient list into a numpy array
# def open_gradient(gradient_output):
#     # Open gradient.txt file and output the data as a list
#     with open(gradient_output, 'r') as file:
#         gradient_output = file.read()

#     # Convert data from the .txt file into an array
#     gradient_lst = ast.literal_eval(gradient_output) # Convert the data from a string to a list
#     gradient_arr = np.array(gradient_lst) # Convert list to an array
#     # print(gradient_arr)

#     return gradient_arr


# gradient_arr = open_gradient(gradient_output)
# print(gradient_arr)

# # Retrieve optimised couplings (PRACTICE)
# optimised_couplings = ['349', '349']
# optimised_couplings_arr = np.array([int(coupling) for coupling in optimised_couplings])
# print(optimised_couplings_arr)

# def update_couplings(gradient_arr, optimised_couplings_arr, stepsize=):

#     # Calculate new couplings by ascending gradient
#     new_couplings_arr = optimised_couplings_arr + stepsize * gradient_arr
#     print(new_couplings_arr)

#     # Convert new couplings to an array of integers
#     new_couplings_arr = np.array([round(float(coupling)) for coupling in new_couplings_arr])

#     return new_couplings_arr

# updated_couplings = update_couplings(gradient_arr, optimised_couplings_arr)
# print(updated_couplings)


##############
# REAL
##############

# List all folders under a specific path
def list_dirs(path):
    dirs = os.listdir(path)
    return dirs

# Looks for most recent gradient output.txt file
def get_gradient_file(dirs):

    for file in dirs:
        if file.startswith('gradient-'):
            file_creation_time = os.path.getctime(file)
            if time.time() - file_creation_time <= 60:
                gradient_output = file
    return gradient_output

# Opens gradient.txt file and convert the gradient list into a numpy array
def open_gradient(gradient_output):
    # Open gradient.txt file and output the data as a list
    with open(gradient_output, 'r') as file:
        gradient_output = file.read()

    # Convert data from the .txt file into an array
    gradient_lst = ast.literal_eval(gradient_output) # Convert the data from a string to a list
    gradient_arr = np.array(gradient_lst) # Convert list to an array
    # print(gradient_arr)

    return gradient_arr

# Gets optimised GA couplings from genome_adjuster.py 
def get_couplings():
    
    # Retrieve coupling values
    optimised_couplings_lst = genome_adjuster.couplings
    optimised_couplings_arr = np.array(optimised_couplings_lst)
    
    return optimised_couplings_lst, optimised_couplings_arr

# Updates couplings using gradient ascent
def update_couplings(gradient_arr, optimised_couplings_arr, stepsize=1000):
    # Calculate new couplings by ascending gradient
    new_couplings_lst = optimised_couplings_arr + stepsize * gradient_arr
    # print(new_couplings_lst)

    # Convert new couplings to a list of integers
    new_couplings_lst = [round(float(coupling)) for coupling in new_couplings_lst]

    return new_couplings_lst

# Reconstruct updated genome based on new couplings
# def reconstruct_genomes(new_couplings)


################
# RUN PROGRAMME
################

# Specify spinchain path
spinchain_path = r'/home/hgjones9/spinchain'

# List folders under spinchain_path
dirs = list_dirs(spinchain_path)
# print(dirs)

# Find most recent gradient.txt file
gradient_output_file = get_gradient_file(dirs)
print(f"Gradient output file: {gradient_output_file}")

# Open gradient.txt file and retrieve the gradient vector as a numpy array
gradient_arr = open_gradient(gradient_output_file)
print(f"Gradient vector: {gradient_arr}")

# Retrieve optimised couplings from genome_adjuster.py 
optimised_couplings_lst, optimised_couplings_arr = get_couplings()
print(f"GA optimised couplings: {optimised_couplings_lst}")

# Update couplings using gradient ascent
new_couplings_lst = update_couplings(gradient_arr, optimised_couplings_arr)
print(f"New couplings: {new_couplings_lst}")
# print(type(new_couplings))




























