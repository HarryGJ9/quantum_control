# Plot Fidelity vs generation 

import matplotlib.pyplot as plt
import numpy as np
import os

# Directory path
base_dir = '/home/hgjones9/quantum_control'

# Pick out relevant fidelity_lst.txt files
fidelity_files = [file for file in os.listdir(base_dir) if file.startswith('fidelity_lst_')]

# Debug output: List the fidelity files found
print("Fidelity files:", fidelity_files)

fidelity_data = []

# Read data from each file
for file in fidelity_files:
    file_path = os.path.join(base_dir, file)
    with open(file_path, 'r') as f:
        line = f.readline().strip()
        y_values = list(map(float, line.split()))
        fidelity_data.append(y_values)

# Create a common x-axis based on the maximum length of the y data
x_length = max(len(y) for y in fidelity_data)
x = np.linspace(0, x_length-1, x_length)

# Plot the data
plt.figure(figsize=(10, 6))

genomes = []

# Get all initial genomes for labeling
for dir_name in os.listdir(base_dir):
    if dir_name.startswith('output_genome_'):
        genetic_out_path = os.path.join(base_dir, dir_name, 'genetic.out')
        print(f"Processing {genetic_out_path}")  # Debug output
        try:
            with open(genetic_out_path, 'r') as f:
                for line in f:
                    if "best genome" in line:
                        genome_full = line.split(':')[1].strip()
                        genomes.append(genome_full)
                        print(f"Found genome: {genome_full}")  # Debug output
                        break  # Assuming there's only one "best genome" line per file
        except FileNotFoundError:
            print(f"File not found: {genetic_out_path}")

# Debug output: List the genomes found
print("Genomes:", genomes)

# Check if the number of genomes matches the number of fidelity files
if len(genomes) != len(fidelity_data):
    print(f"Warning: Number of genomes ({len(genomes)}) does not match number of fidelity data sets ({len(fidelity_data)}).")


# Plot each dataset with different styles
for i, y in enumerate(fidelity_data):
    plt.plot(x[:len(y)], y, label=f'Genome: {genomes[i]}')

# Add title and labels
plt.title('Fidelity vs Iteration')
plt.xlabel('Iteration')
plt.ylabel('Fidelity')

# Add legend
plt.legend()

# Show grid
plt.grid(True)

# Show the plot
plt.show()


# # Convert to list of integers
# iteration_lst = [int(iteration) for iteration in iterations]

# # Read contents from fidelity_lst.txt
# with open('/home/hgjones9/quantum_control/fidelity_lst.txt', 'r') as file:
#     fidelities = file.read().strip().split()

# # Convert to list of integers
# fidelity_lst = [float(fidelity) for fidelity in fidelities]

# # Convert to array of integers ready for plotting
# iteration_arr = np.arange(0, max_iterations + 1)
# fidelity_arr = np.array(fidelity_lst)

# # Plot fidelity vs iterations
# plt.plot(iteration_arr, fidelity_arr)
# plt.title('Fidelity vs Iteration Number')
# plt.ylabel('Fidelity')
# plt.xlabel('Iteration')
# plt.savefig('fidelity_iteration.pdf')
# plt.show()






