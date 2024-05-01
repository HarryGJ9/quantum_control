import re
import os
import datetime

# This script takes in the optimised genome found by the GA as an input and returns a list of 
# genomes that have had their individual couplings altered by the derivative step size

# Obtains optimised genome from the GA
def find_genome(output_path):
    # Open genetic.out and find the genome
    with open(output_path, 'r') as file:
        for line in file:
            if "best genome" in line:
                genome_full = line.split(':')[1].strip()
                # print(f'GA output genome: {genome_full}')
    return genome_full

# Obtains un-optimised genome from just spinnet
# def find_genome(output_path):
#     # Open genetic.out and find the genome
#     with open(output_path, 'r') as file:
#         for line in file:
#             if "initial genome" in line:
#                 genome_full = line.split(':')[1].strip()
#                 # print(f'GA output genome: {genome_full}')
#     return genome_full


# Extracts the couplings from the genome and adjusts couplings
def adjust_couplings(genome_full, h=100):
    # Obtain couplings from the genome
    genome = genome_full.split('#')[0].split('>')[1].replace('"', '') # Remove the <i|f> directive and any digit after the '#' 
    couplings = re.findall(r'\d+', genome) # Find all couplings
    couplings = [int(coupling) for coupling in couplings] # Convert each coupling to an integer and return as a list
    # print(f"Couplings = {couplings}")

    # For each coupling, calculate (coupling + h) and (coupling - h) and store them in a lsit
    couplings_plus_h = [coupling + h for coupling in couplings]
    couplings_minus_h = [coupling - h for coupling in couplings]

    return genome, couplings, couplings_plus_h, couplings_minus_h

# Normalise adjusted couplings to all be the same number of digits and change any negative values to 0
def normalise_couplings(couplings):

    # Check if a four digit coupling is present
    four_digit_present = any(coupling >= 1000 for coupling in couplings)

    # Add a '0' in front of any two digit number, or change any negative numbers to 0
    for i in range(len(couplings)):
        if 0 < couplings[i] < 100:
            couplings[i] = f'{couplings[i]:03d}'
        elif couplings[i] <= 0:
            couplings[i] = '001'

    # If four digit coupling present, add a '0' at the start
    if four_digit_present:
        for i in range(len(couplings)):
            # print(f'Coupling: {couplings[i]}')
            # print(f'Type: {type(couplings[i])}')
            couplings[i] = int(couplings[i])
            if 100 <= couplings[i] < 1000:
                couplings[i] = f'{couplings[i]:04d}'
            elif 0 < couplings[i] < 100:
                couplings[i] = f'{couplings[i]:04d}'
            elif couplings[i] <= 0:
                couplings[i] = '0001'

    return couplings



# Constructs new genomes based on the adjusted couplings
def construct_new_genomes(genome, couplings_plus_h, couplings_minus_h):
    # Split genome into a list of characters and couplings
    genome_split = re.split(r'([A-Za-z]+|\d+)', genome)
    genome_list = [index for index in genome_split if index]
    # print(f"Genomes split into characters and couplings = {genome_list}")
    
    # Normalise adjusted couplings to ensure all couplings have the same number of digits
    adjusted_couplings = couplings_plus_h + couplings_minus_h # Concatenate lists
    # print(f'Concatenated couplings: {adjusted_couplings}')
    adjusted_couplings = normalise_couplings(adjusted_couplings) # Normalise whole list
    # print(f'Concatenated couplings normalised: {adjusted_couplings}')
    midpoint = len(adjusted_couplings) // 2 # Calculate midpoint of list
    
    # Split back into two lists
    couplings_plus_h = adjusted_couplings[:midpoint]
    couplings_minus_h = adjusted_couplings[midpoint:]
    # print(f'Couplings + h: {couplings_plus_h}')
    # print(f'Couplings - h: {couplings_minus_h}')

    # Compile new genomes based on adjusted couplings and letter characters of previous genome
    adjusted_genomes = []

    # Iterate over genome_split and construct new genomes
    for index, item in enumerate(genome_split):
        if item.isdigit(): # Checks if the item is a coupling
            plus_h = str(couplings_plus_h.pop(0)) # Remove the first element from the list couplings_plus_h and save it
            #print(plus_h)
            minus_h = str(couplings_minus_h.pop(0)) # Same again with coupling_minus_h
            
            # Construct new genomes by joining the previous characters up to the current index, with the new coupling
            # Then add the rest of the genome onto it
            genome_plus_h = ''.join(genome_split[:index]) + plus_h + ''.join(genome_split[index + 1:])
            genome_minus_h = ''.join(genome_split[:index]) + minus_h + ''.join(genome_split[index + 1:])
            
            # Add adjusted genomes to a single list
            adjusted_genomes.extend([genome_plus_h, genome_minus_h])
    
    return genome_list, adjusted_genomes

# Normalise adjusted genomes
def normalise_genome(genome):

    # Split the genome string into characters and couplings of letters and digits
    split_genome = re.findall(r'[A-Za-z]+|\d+', genome)
    
    # Separate the characters and digits into different lists
    characters = [item for item in split_genome if item.isalpha()]
    couplings = [int(item) for item in split_genome if item.isdigit()]
    # print(characters)
    # print(couplings)

    # Normalise couplings
    couplings_norm = normalise_couplings(couplings)
    # print(couplings_norm)

    # Merge genome
    adjusted_genome = ''.join([f'{character}{coupling}' for character, coupling in zip(characters, couplings)])
    # print(adjusted_genome)

    return adjusted_genome


###############
# RUN PROGRAMME
###############

# Directory of the output genome
output_path = r'/home/hgjones9/quantum_control/output-latest/genetic.out'

# Extract full optimised genome (inclduing <i|f> directive) from the GA output
genome_full = find_genome(output_path)
print(f"Full genome: {genome_full}")

# Strip full genome and adjust the couplings in preparation of derivative calculation
GA_genome, GA_couplings, couplings_plus_h, couplings_minus_h = adjust_couplings(genome_full)
print(f"Stripped genome: {GA_genome}")

# Reconstruct genomes based on the adjusted couplings
genome_list, adjusted_genomes = construct_new_genomes(GA_genome, couplings_plus_h, couplings_minus_h)
# print(f"Adjusted genomes: {adjusted_genomes}")

# Ensure all adjusted genomes have normalised couplings
adjusted_genomes_norm = []
for genome in adjusted_genomes:
    adjusted_genome = normalise_genome(genome)
    adjusted_genomes_norm.append(adjusted_genome)

print(f'Normalised adjusted genomes: {adjusted_genomes_norm}')

# Write the original optimised genome and adjusted couplings to a .txt file
with open(f'/home/hgjones9/quantum_control/initial_adjusted_genomes.txt', 'w') as file:
    # Write content to the file
    file.write(f"GA optimised genome : {GA_genome}\n")
    file.write(f"Isolated couplings : {GA_couplings}\n")
    file.write(f"Adjusted genomes : {adjusted_genomes_norm}\n")



