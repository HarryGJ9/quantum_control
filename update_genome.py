import os
import numpy as np
import time
import datetime
import ast
# import genome_adjuster
import re
from genome_adjuster import GA_couplings
# from genome_adjuster import GA_genome


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
    
    # Retrieve coupling valuesgenome_adjuster
    optimised_couplings_lst = GA_couplings
    optimised_couplings_arr = np.array(optimised_couplings_lst)
    
    return optimised_couplings_lst, optimised_couplings_arr

# # Updates couplings using gradient ascent
# def update_couplings(gradient_arr, optimised_couplings_arr, stepsize=1e5):
#     # Calculate new couplings by ascending gradient
#     new_couplings_lst = optimised_couplings_arr + stepsize * gradient_arr
#     # print(new_couplings_lst)

#     # Convert new couplings to a list of integers
#     new_couplings_lst = [round(float(coupling)) for coupling in new_couplings_lst]

#     return new_couplings_lst

# # Reconstruct new genome based on new couplings
# def reconstruct_genome(origin_genome, new_couplings):

#     # Split original, optimised gnome (e.g. "AB500BC500") into a list of characters and digits (e.g. ['AB', '500', 'BC', '500'])
#     genome_split = re.split(r'([A-Za-z]+|\d+)', origin_genome)

#     # Iterate through list and swap the original couplings for the new couplings (e.g. ['AB', '450', 'BC', '450'])
#     new_genome_lst = []
#     for idx, item in enumerate(genome_split):
#         if item.isdigit():
#             new_genome_lst.append(new_couplings.pop(0))
#         else:
#             new_genome_lst.append(item)
    
#     new_genome = ''.join(str(item) for item in new_genome_lst)

#     return new_genome

# # Returns current date and time (used to write file)
# def current_time():
    
#     current_time = datetime.datetime.now()
#     year = current_time.year
#     month = current_time.month
#     day = current_time.day
#     hour = current_time.hour
#     min = current_time.minute
#     sec = current_time.second

#     return year, month, day, hour, min, sec

################
# RUN PROGRAMME
################

# Specify quantum_control path
quant_cont_path = '/home/hgjones9/quantum_control'

# List folders under quantum_control
dirs = list_dirs(quant_cont_path)
# print(dirs)

# Find most recent gradient.txt file
gradient_output_file = get_gradient_file(dirs)
print(f"Gradient output file: {gradient_output_file}")

# Open gradient.txt file and retrieve the gradient vector as a numpy array
gradient_arr = open_gradient(gradient_output_file)
print(f"Gradient vector: {gradient_arr}")

# # Retrieve optimised couplings from genome_adjuster.py 
# optimised_couplings_lst, optimised_couplings_arr = get_couplings()
# print(f"GA optimised couplings: {optimised_couplings_lst}")

# # Update couplings using gradient ascent
# new_couplings_lst = update_couplings(gradient_arr, optimised_couplings_arr)
# print(f"New couplings: {new_couplings_lst}")
# # print(type(new_couplings))

# # Reconstruct new genome based on grad ascent updated couplings
# new_genome = reconstruct_genome(genome_adjuster.genome, new_couplings_lst)
# print(new_genome)

# # Write new genome to an output .txt file
# with open(f'/home/hgjones9/quantum_control/new_genome.txt', 'w') as file:
#     file.write(new_genome)

# # Retrieve current times
# year = current_time()[0]
# month = current_time()[1]
# day = current_time()[2]
# hour = current_time()[3]
# min = current_time()[4]
# sec = current_time()[5]

# # Write new genome to an output file
# with open(f'/home/hgjones9/spinchain/new_genome-{year}-{month}-{day}-{hour}-{min}-{sec}.txt', 'w') as file:
#     file.write(str(new_genome))






























