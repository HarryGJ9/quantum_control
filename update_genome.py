import os
import numpy as np
import time
import datetime
import ast
import re
import sys

# List all folders under a specific path
def list_dirs(path):
    dirs = os.listdir(path)
    return dirs

# Looks for most recent gradient_latest.txt file
def get_gradient_file(dirs):

    for file in dirs:
        if file.startswith('gradient_latest'):
            gradient_output_file = file


    return gradient_output_file

# Opens gradient.txt file and convert the gradient list into a numpy array
def open_gradient(gradient_output_file):
    # Open gradient.txt file and output the data as a list
    with open(gradient_output_file, 'r') as file:
        gradient_output = file.read()

    # Convert data from the .txt file into an array
    gradient_lst = ast.literal_eval(gradient_output) # Convert the data from a string to a list
    gradient_arr = np.array(gradient_lst) # Convert list to an array
    

    return gradient_arr

# Obtain old couplings ready to be updated
def extract_old_couplings():

    with open(os.path.join(quant_cont_path, 'old_couplings.txt'), 'r') as file:
        old_couplings_str = file.read()
        
    # Convert literal string from file into a python list
    old_couplings_lst = ast.literal_eval(old_couplings_str)
   
    # Convert old_couplings_lst to an array
    old_couplings_arr = np.array([int(x) for x in old_couplings_lst])
    
    return old_couplings_lst, old_couplings_arr

# Ensure all couplings are normalised to the same number of digits (padded by 0s)
def normalise_couplings(couplings):

    # Make sure all couplings are integers
    couplings = [int(coupling) for coupling in couplings]

    # Check if a four digit coupling is present
    four_digit_present = any(coupling >= 1000 for coupling in couplings)
    print(f'Four digit present: {four_digit_present}')

    # Add a '0' in front of any two digit number, or change any negative numbers to 0
    for i in range(len(couplings)):
        if 0 <= couplings[i] < 100:
            couplings[i] = f'{couplings[i]:03d}'
        elif couplings[i] < 0:
            couplings[i] = '000'
    
    # If four digit coupling present, add a '0' at the start
    if four_digit_present:
        for i in range(len(couplings)):
            print(f'Coupling: {couplings[i]}')
            print(f'Type: {type(couplings[i])}')
            couplings[i] = int(couplings[i])
            if 100 <= couplings[i] < 1000:
                couplings[i] = f'{couplings[i]:04d}'
            elif 0 <= couplings[i] < 100:
                couplings[i] = f'{couplings[i]:04d}'
            elif couplings[i] <= 0:
                couplings[i] = '0000'
    
    return couplings

# Updates couplings using gradient ascent
def update_couplings(gradient_arr, old_couplings_arr, stepsize):
    
    # Calculate new couplings by ascending gradient
    new_couplings_arr = old_couplings_arr + stepsize * gradient_arr
    print(f'New couplings array: {new_couplings_arr}')

    # Convert new couplings array to a list of integers
    new_couplings_lst = [round(float(coupling)) for coupling in new_couplings_arr]
    print(f'New couplings list: {new_couplings_lst}')        

    # Normalise all couplings to have the same number of digits
    new_couplings_lst = normalise_couplings(new_couplings_lst)
    print(f'New couplings list normalised: {new_couplings_lst}')

    return new_couplings_lst

# Reconstruct new genome based on new couplings
def reconstruct_genome(new_couplings_lst):

    # Open initial_adjusted_genomes.txt and find the GA optimised genome
    with open(os.path.join(quant_cont_path, 'initial_adjusted_genomes.txt'), 'r') as file:
        for line in file:
            if line.startswith('GA optimised genome'):
                # Split line to obtain just the genome
                genome = line.split(':')[1].strip()


    # Split original, optimised gnome (e.g. "AB500BC500") into a list of characters and digits (e.g. ['AB', '500', 'BC', '500'])
    genome_split = re.split(r'([A-Za-z]+|\d+)', genome)

    # Iterate through list and swap the original couplings for the new couplings (e.g. ['AB', '450', 'BC', '450'])
    new_genome_lst = []
    for idx, item in enumerate(genome_split):
        if item.isdigit():
            new_genome_lst.append(new_couplings_lst.pop(0))
        else:
            new_genome_lst.append(item)
    
    new_genome = ''.join(str(item) for item in new_genome_lst)

    return new_genome


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

# Extract old couplings ready to be updated
old_couplings_lst, old_couplings_arr = extract_old_couplings()
print(f'Old couplings: {old_couplings_arr}')

# Check if stepsize argument is provided in bash_script.sh, if so adjust stepsize accordingly
if len(sys.argv) > 1:
    stepsize = int(sys.argv[1])
else:
    stepsize = 1e5

# Update couplings using gradient ascent
new_couplings_lst = update_couplings(gradient_arr, old_couplings_arr, stepsize)
print(f"New couplings: {new_couplings_lst}")

# Reconstruct new genome based on grad ascent updated couplings
new_genome = reconstruct_genome(new_couplings_lst)
print(f'New genome: {new_genome}')

# Write new genome to an output .txt file
with open('/home/hgjones9/quantum_control/new_genome.txt', 'w') as file:
    file.write(new_genome)























