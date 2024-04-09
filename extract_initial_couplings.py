import os

# Specify file path
quant_cont_path = '/home/hgjones9/quantum_control/adjusted_genomes.txt'
file_path = os.path.join(quant_cont_path, 'initial_adjusted_genomes.txt')

# Open the file
with open(file_path, 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Check if the line starts with 'Isolated couplings:'
        if line.startswith('Isolated couplings:'):
            # Split the line to extract the list of couplings
            initial_couplings = line.split(':')[1].strip()
            # Print the extracted couplings
            print(initial_couplings)

with open(os.path.join(quant_cont_path), 'initial_couplings.txt', 'w') as file:
    file.write(initial_couplings)