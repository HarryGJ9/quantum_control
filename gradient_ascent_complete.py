import subprocess
import re

######################
# STEP 1:
# Run modified gen alg and obtain top 5 genomes, max fidelities and corresponding times
######################

# Path to spinnet
spinnet_path = "/home/hgjones9/quantum_control/spinchain-ga-genetic/bin/spinnet"

# input arguments, including optimisation flag, number of generations and genome
args = ["-o", "-G", "2", "<A|C>AB100BC900"]

# Run the spinnet optimisation code
result = subprocess.run([spinnet_path] + args, capture_output=True, text=True)

# # Print output
# print("Output from spinnet:")
# print(result.stdout)

# # Check for errors
# if result.stderr:
#     print("Errors: ", result.stderr)

# Obtain the 5 optimised genomes, their maximum fidelities and corresponding times

# genetic.out path
gen_out_path = "/home/hgjones9/quantum_control/output-latest/genetic.out"

# Find pattern to extract useful information from the genetic.out file
pattern = re.compile(
    r'best genome:\s*"([^"]+)"'  # Capture the genome string in quotes
)
# Function to extract the genomes from the genetic.out file, as well as their fidelities and times
def extract_genomes(file_path):
    
    # Read genetic.out file
    with open(file_path, 'r') as file:
        content = file.read()

    # Search for relevant lines using the previously defined regex pattern
    genome_pattern = re.compile(
        r'(\d+(?:st|nd|rd|th) best genome):\s*"([^"]+)"\s+with fitness:\s+([\d.]+)\s+\(([\d.]+)% fidelity.*time\s+([\d.]+)\)'
        )
    
    # Pattern for the first best genome
    first_best_genome_pattern = re.compile(
        r'best genome:\s*"([^"]+)"\s+with fitness:\s+([\d.]+)\s+\(([\d.]+)% fidelity.*time\s+([\d.]+)\)'
        )
    
    # Read the file and search for matches
    with open(file_path, 'r') as f:
        content = f.read()  # Read the entire file

        # Find all matches in the content
        matches = genome_pattern.findall(content)

    # Check for the first best genome
    first_best_match = first_best_genome_pattern.search(content)
    best_genomes_info = []

    # Add the first best genome if found
    if first_best_match:
        genome, fitness, fidelity, time = first_best_match.groups()
        best_genomes_info.append({
            'rank': 'best genome',  # Changed to 'best genome'
            'genome': genome,
            'fitness': float(fitness),
            'fidelity': float(fidelity),
            'time': float(time)
        })

    # Append subsequent matches
    for rank, genome, fitness, fidelity, time in matches:
        best_genomes_info.append({
            'rank': rank,
            'genome': genome,
            'fitness': float(fitness),
            'fidelity': float(fidelity),
            'time': float(time)
        })

    return best_genomes_info

# Extract information from genetic.out file and print
best_genomes_info = extract_genomes(gen_out_path)
# print(best_genomes_info)

for genome_info in best_genomes_info:
    print(f"{genome_info['rank']}: {genome_info['genome']} with {genome_info['fidelity']} at {genome_info['time']}s")


