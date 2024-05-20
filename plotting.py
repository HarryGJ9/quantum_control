# Plot Fidelity vs generation 

import matplotlib.pyplot as plt
import numpy as np

# Read contents from iteration_lst.txt
with open('/home/hgjones9/quantum_control/iteration_lst.txt', 'r') as file:
    iterations = file.read().strip().split()

# Convert to list of integers
iteration_lst = [int(iteration) for iteration in iterations]

# Read contents from fidelity_lst.txt
with open('/home/hgjones9/quantum_control/fidelity_lst.txt', 'r') as file:
    fidelities = file.read().strip().split()

# Convert to list of integers
fidelity_lst = [float(fidelity) for fidelity in fidelities]


# Convert to array of integers ready for plotting
iteration_arr = np.array(iteration_lst)
fidelity_arr = np.array(fidelity_lst)

# Plot fidelity vs iterations
plt.plot(iteration_arr, fidelity_arr)
plt.title('Fidelity vs Iteration Number')
plt.ylabel('Fidelity')
plt.xlabel('Iteration')
plt.savefig('fidelity_iteration.pdf')
plt.show()






