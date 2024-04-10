import os
import re

# Specify quantum_control path
quant_cont_path = '/home/hgjones9/quantum_control'

# Obtain most recent updated (now old) genome
def find_new_genome():
    
    # Open latest new_genome.txt file
    with open(os.path.join(quant_cont_path, 'new_genome.txt'), 'r') as file:
        new_genome_str = file.read()
    
    return new_genome_str

# Extract couplings from genome and adjust couplings
def adjust_couplings(genome_str, h=100):
    
    # Obtain couplings from genome
    couplings = re.findall(r'\d+', genome_str) # Find all couplings
    couplings_lst = [int(coupling) for coupling in couplings] # Convert each coupling to an integer and stor in a list

    # For each coupling, calculate (coupling + h) and (coupling - h) and store in a list
    couplings_plus_h = [coupling + h for coupling in couplings]
    couplings_minus_h = [coupling - h for coupling in couplings]

    return couplings_plus_h, couplings_minus_h

# Construct new genomes based on adjusted couplings
def construct_new_genomes(genome_str, couplings_plus_h, couplings_minus_h):
    # Split genome into a list of characters and couplings
    genome_split = re.split(r'([A-Za-z]+|\d+)', genome_str)
    genome_list = [index for index in genome_split if index]
    # print(f"Genomes split into characters and couplings = {genome_list}")

    # Compile new genomes based on adjusted couplings and letter characters of previous genome
    adjusted_genomes = []

    # Iterate over genome_split and construct new genomes
    for index, item in enumerate(genome_split):
        if item.isdigit(): # Checks if the item is a coupling
            plus_h = str(couplings_plus_h.pop(0)) # Remove the first element from the list couplings_plus_h and save it
            minus_h = str(couplings_minus_h.pop(0)) # Same again with coupling_minus_h
            
            # Construct new genomes by joining the previous characters up to the current index, with the new coupling
            # Then add the rest of the genome onto it
            genome_plus_h = ''.join(genome_split[:index]) + plus_h + ''.join(genome_split[index + 1:])
            genome_minus_h = ''.join(genome_split[:index]) + minus_h + ''.join(genome_split[index + 1:])
            
            # Add adjusted genomes to a single list
            adjusted_genomes.extend([genome_plus_h, genome_minus_h])

    return genome_list, adjusted_genomes

###############
# RUN PROGRAMME
###############

# Extract most recent updated genome
new_genome = find_new_genome()
print(f'New genome: {new_genome}')

# Adjust couplings in preparation for central diff calculation
couplings_plus_h, couplings_minus_h = adjust_couplings(new_genome)

# Reconstruct genomes based on adjusted couplings
adjusted_genomes = construct_new_genomes
print(f'Adjusted genomes: {adjusted_genomes}')

# Write adjusted genomes to a file 
with open(os.path.join(quant_cont_path, 'adjusted_genomes.txt'), 'w') as file:
    file.write(f"Adjusted genomes : {adjusted_genomes}")