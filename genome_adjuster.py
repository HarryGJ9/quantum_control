import re

# This script takes in the optimised genome found by the GA as an input and returns a list of 
# genomes that have had their individual couplings altered by the derivative step size

#########################
# OBTAIN OUTPUTTED GENOME
#########################

# Directory of the output genome
output_path = r'/home/hgjones9/quantum_control/output-latest/genetic.out'

# Open genetic.out and find the genome
with open(output_path, 'r') as file:
    for line in file:
        if "best genome" in line:
            genome_full = line.split(':')[1].strip("")
            print(f'GA output genome: {genome_full}')

# # Test genome
# genome_full = "<A|C>AB500BC450#00"

##################
# ADJUST COUPLINGS 
##################
            
# Obtain couplings from the genome
genome = genome_full.split('#')[0].split('>')[1] # Remove the <i|f> directive and any digit after the '#' 
couplings = re.findall(r'\d+', genome) # Find all couplings
couplings = [int(coupling) for coupling in couplings] # Convert each coupling to an integer and return as a list
print(f"Couplings = {couplings}")

# For each coupling, calculate (coupling + h) and (coupling - h) and store them in a lsit
h = 5 # Derivative stepsize
couplings_plus_h = [coupling + h for coupling in couplings]
couplings_minus_h = [coupling - h for coupling in couplings]

print(f"Couplings + h = {couplings_plus_h}")
print(f"Couplings - h = {couplings_minus_h}")


##################################################
# GENERATE NEW GENOMES BASED ON ADJUSTED COUPLINGS
##################################################

# Split genome into a list of characters and couplings
genome_split = re.split(r'([A-Za-z]+|\d+)', genome)
genome_list = [index for index in genome_split if index]
print(f"Genomes split into characters and couplings = {genome_list}")


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

print(f"Adjusted genomes: {adjusted_genomes}")


# # Write all relevant data to an output .txt file
# with open('output.txt', 'w') as file:
#     # Write content to the file
#     file.write(f"GA optimised genome = {genome}\n")
#     file.write(f"Adjusted genomes = {adjusted_genomes}\n")

    







