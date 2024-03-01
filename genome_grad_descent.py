# Start with an input genome 
# Calculate the fidelity of the genome wrt final state
# Calculate the fitness of the genome (initialises starting point)
# for a certain number of iterations:
    # calculate gradient wrt coupling 
    # if gradient ~ 0: break    
    # update the genome by current_coupling - learning_rate * gradient
    # calculate fidelity of new genome wrt final state
    # calculate fitness of new genome
    # output optimised genome, its fidelity and fitness

import numpy as np
import cmath
import re

#############################
# START WITH GA OUTPUT GENOME
#############################

# Directory of the output genome
output_path = r'/home/hgjones9/spinchain/output-latest/genetic.out'

# Open genetic.out and find the genome
with open(output_path, 'r') as file:
    for line in file:
        if "best genome" in line:
            genome = line.split(':')[1].strip()
            print(f'GA output genome: {genome}')


############################################################################
# CALCULATE THE FIDELITY OF OUTPUT GENOME WRT FINAL STATE AT A SPECIFIC TIME  
############################################################################
            
# FOLLOWING CODE (LINES 36-68) IS FROM STATIC_FIDELITY.PY

# Specify path to dynamics_formatted.data
dynamics_path = r'/home/hgjones9/spinchain/output-latest/data/dynamics_formatted.data'

# Create empty dictionary in which to add fidelity at a specified time
fidelities = {}

# Open and read file
with open(dynamics_path, 'r') as file:

    next(file) # Skip the first line as this is the title

    # For each row of data, strip edge whitespace and separate by one whitespace
    for row in file:
        values = row.strip().split()

        # If there are values in the row (i.e. not blank space):
        # Return the time, rounded to 2 d.p.
        # Append the dictionary to include the fidelity value at a specific time
        if values:
            time = round(float(values[0]), 2)
            fidelity_value = complex(values[2])
            fidelities[time] = np.linalg.norm(fidelity_value)

# Specify time at which to calculate fidelity
target_time = float(input("Input time (to 1 d.p.) to calculate fidelity: "))

# Check that the time given is in the given data range
if target_time > 20 or target_time < 0:
    raise Exception("Time must be between 0 and 20")

# Return fidelity at the target time
fidelity = fidelities[target_time]
print(f"Fidelity wrt to target state at t={target_time} is {fidelity:.2f}")


# #####################################
# # CALCULATE FITNESS OF OUTPUT GENOME 
# #####################################

def fitness(fidelity, time, a=10, b=-0.001, Jmax=1):
    return 100 * np.exp(a * (fidelity - 1)) * np.exp(b * time * Jmax)

initial_fitness = fitness(fidelity, target_time)

# ###################################################
# # DO GRADIENT DESCENT, STARTING WITH INITIAL GENOME
# ###################################################

# # Define maximum number of iterations before GD terminates
# max_iterations = 100

# Obtain the coupling values to calculate gradient of fitness
genome_split = genome.split('#')[0] # Remove any digit after the '#'
couplings = re.findall(r'\d+', genome_split) # Find all couplings, return them as a list of strings
couplings = [int(coupling) for coupling in couplings] # Convert each coupling to an integer
print(couplings)

# # Define parameters
# h = 0.01 # Define gradient step size
# gradients = [] # Initialise empty list into which coupling gradients are added
# threshold = 1e-6 # Define threshold to determine if gradient is sufficiently small
# learning_rate = 0.01 # Learning rate for the GD algorithm

# for _ in (max_iterations):

#     # Calculate the numerical derivative of each coupling
#     for coupling in couplings:
#         calculate_gradient = ((coupling + h) - (coupling - h)) / (2 * h)
#         gradients.append(calculate_gradient)
    
#     # Calculate the norm of the gradient vector 
#     gradient_norm = np.linalg.norm(gradients)

#     # If the gradient is small enough, terminate the descent
#     if gradient_norm < threshold:
#         break

    
    # Now: do I need to calculate the dynamics of the system to determine a new fitness/fidelity/both?
    # If so, is there a way I can just call 'dynamics' with the genome being the input?
    # Instead of simply running 'spinnet' again?
    # Also: am I extremising the fitness or fidelity? 







