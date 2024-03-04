
import numpy as np
import cmath
import re

#########################
# OBTAIN OUTPUTTED GENOME
#########################

# # Directory of the output genome
# output_path = r'/home/hgjones9/spinchain/output-latest/genetic.out'

# # Open genetic.out and find the genome
# with open(output_path, 'r') as file:
#     for line in file:
#         if "best genome" in line:
#             genome = line.split(':')[1].strip()
#             print(f'GA output genome: {genome}')

# Test genome
genome_full = "AB500BC450#00"


##################
# ADJUST COUPLINGS 
##################
            
# Obtain couplings from the genome
genome = genome_full.split('#')[0] # Remove any digit after the '#'
couplings = re.findall(r'\d+', genome) # Find all couplings, return them as a list of strings
couplings = [int(coupling) for coupling in couplings] # Convert each coupling to an integer
print(couplings)


# Adjust couplings by +/- h and store them in a list
couplings_plus_h = [] # Initialise empty list to store J + h values
couplings_minus_h = [] # Initialise empty list to store J - h values
h = 5 # Derivative stepsize

# For each coupling, calculate (coupling + h) and (coupling - h) and append to relevant list
for coupling in couplings:
    couplings_plus_h.append(coupling + h)
    couplings_minus_h.append(coupling - h)

print(couplings_plus_h)
print(couplings_minus_h)


##################################################
# GENERATE NEW GENOMES BASED ON ADJUSTED COUPLINGS
##################################################

# Split genome into letters and numbers
genome_split = re.split(r'\d+', genome)
print(genome_split)

# Obtain the letter characters from the genome 
letters = [substring for substring in genome_split if substring]
print(letters)

# Compile a new genome based on adjusted couplings and letter characters of previous 

adjusted_genomes = []
for index, letter_pair in enumerate(genome_split):
    
    # Identify adjusted couplings
    plus_h = couplings_plus_h[index]
    minus_h = couplings_minus_h[index]

    # Construct new genomes
    genome_plus_h = letter_pair + str(plus_h) + "BC" + str(couplings[index+1]%len(genome_split)[1])
    genome_minus_h = letter_pair + str(plus_h) + "BC" + str(minus_h)
    adjusted_genomes.extend([genome_plus_h, genome_minus_h])

print(adjusted_genomes) 



    







