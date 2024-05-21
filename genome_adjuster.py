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
def adjust_couplings(genome_str, h=0.1):
    
    # Obtain couplings from genome
    couplings = re.findall(r'\d+', genome_str) # Find all couplings
    couplings_lst = [int(coupling) for coupling in couplings] # Convert each coupling to an integer and stor in a list

    # Calculate adjusted couplings and store in two separate lists
    couplings_plus_h = [round(float(coupling) * (1 + h)) for coupling in couplings]
    couplings_minus_h = [round(float(coupling) * (1 - h)) for coupling in couplings]

    return couplings_plus_h, couplings_minus_h

# Normalise adjusted couplings to all be the same number of digits
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


# Construct new genomes based on adjusted couplings
def construct_new_genomes(genome_str, couplings_plus_h, couplings_minus_h):
    # Split genome into a list of characters and couplings
    genome_split = re.split(r'([A-Za-z]+|\d+)', genome_str)
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

# Extract most recent updated genome
new_genome = find_new_genome()
print(f'New genome: {new_genome}')

# Adjust couplings in preparation for central diff calculation
couplings_plus_h, couplings_minus_h = adjust_couplings(new_genome)
# print(f"Adjusted couplings: {couplings_plus_h}, {couplings_minus_h}")

# Reconstruct genomes based on adjusted couplings
genome_lst, adjusted_genomes = construct_new_genomes(new_genome, couplings_plus_h, couplings_minus_h)
# print(f'Adjusted genomes: {adjusted_genomes}')

# Ensure all adjusted genomes have normalised couplings
adjusted_genomes_norm = []
for genome in adjusted_genomes:
    adjusted_genome = normalise_genome(genome)
    adjusted_genomes_norm.append(adjusted_genome)

# print(f'Normalised adjusted genomes: {adjusted_genomes_norm}')

# Write adjusted genomes to a file 
with open(os.path.join(quant_cont_path, 'adjusted_genomes.txt'), 'w') as file:
    file.write(f"Adjusted genomes : {adjusted_genomes_norm}")