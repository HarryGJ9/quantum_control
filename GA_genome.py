"""
Script obtains the GA optimised genome and saves it to a .txt file

"""
import sys

# Obtains optimised genome from either the GA or an input genome
def find_genome(output_path, GA):
    # Open genetic.out and find the genome
    with open(output_path, 'r') as file:
        for line in file:
            if GA == "y":
                if "best genome" in line:
                    genome_full = line.split(':')[1].strip()
                    # print(f'GA output genome: {genome_full}')
            elif GA == "n":
                if "initial genome" in line:
                    genome_full = line.split(':')[1].strip()

    genome = genome_full.split('#')[0].split('>')[1].replace('"', '') # Remove the <i|f> directive and any digit after the '#' 
    
    return genome

# User chooses GA optimisation or not
GA = str(sys.argv[1])
GA_genome = find_genome('/home/hgjones9/quantum_control/output-latest/genetic.out', GA)

# Write new genome to an output .txt file
with open('/home/hgjones9/quantum_control/new_genome.txt', 'w') as file:
    file.write(GA_genome)