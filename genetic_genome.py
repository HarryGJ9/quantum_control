"""
Script obtains the GA optimised genome and saves it to a .txt file

"""
import sys

# Obtains optimised genome from either the GA or an input genome
def find_genome(output_path, gen_alg):
    # Open genetic.out and find the genome
    with open(output_path, 'r') as file:
        for line in file:
            if gen_alg == "y":
                if "best genome" in line:
                    genome_full = line.split(':')[1].strip()
                    # print(f'GA output genome: {genome_full}')
            elif gen_alg == "n":
                if "initial genome" in line:
                    genome_full = line.split(':')[1].strip()

    genome = genome_full.split('#')[0].split('>')[1].replace('"', '') # Remove the <i|f> directive and any digit after the '#' 
    
    return genome

# User chooses genetic alg optimisation or not
gen_alg = str(sys.argv[1])
genome_num = str(sys.argv[2])
genetic_genome = find_genome('/home/hgjones9/quantum_control/output_genome_' + genome_num + '/genetic.out', gen_alg)


# Write new genome to an output .txt file
with open('/home/hgjones9/quantum_control/new_genome_' + genome_num + '.txt', 'w') as file:
    file.write(genetic_genome)

# # Obtain genetic optimised genome
# gen_alg = sys.argv[1]
# genetic_genome = find_genome('/home/hgjones9/quantum_control/output-latest/genetic.out', gen_alg)
# print(genetic_genome)