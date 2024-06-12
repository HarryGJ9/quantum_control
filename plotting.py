# Plot Fidelity vs generation 

import matplotlib.pyplot as plt
import numpy as np
import os

# Pick out relevant fidelity_lst.txt files
fidelity_files = []
dirs = os.listdir('/home/hgjones9/quantum_control')
for file in dirs:
    if file.startswith('fidelity_lst_'):
        fidelity_files.append(file)


        # with open(file, 'r') as file:
        #     # fidelities = file.read().strip().split()

fidelity_data = []
# Read data from each file
for file in fidelity_files:
    with open(file, 'r') as file:
        line = file.readline().strip()
        y_values = list(map(float, line.split()))
        fidelity_data.append(y_values)

# Create a common x-axis based on the maximum length of the y data
x_length = max(len(y) for y in fidelity_data)
x = np.linspace(0, x_length-1, x_length)

# Plot the data
plt.figure(figsize=(10, 6))

genomes = []
# Get all initial genomes for labelling
for file in dirs:
    if file.startswith('output_genome_'):
        print(file)
        with open(os.path.join('/home/hgjones9/quantum_control/', file, 'genetic.out'), 'r') as file:
            if "best genome" in line:
                genome_full = line.split(':')[1].strip()
                print(genome_full)
                genomes.append(genome_full)

print(genomes)

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






