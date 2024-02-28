#!/bin/bash

# User provides genome sequence
# echo "Enter genome sequence: "
# read genome

# # Users specifies time at which to calculate fitness 
# echo "Enter time at which fitness is evaluated: "
# read time

# Calculate fidelity at specific time



# Compute the fitness function at that time
# a = 10
# b = -0.001
# t = time
# # F = fidelity 
# # Jmax = Jmax

# fitness = $(echo "scale=2; 100 * exp($a * ($F - 1)) * exp($b * $t * $Jmax)" | bc -1)

# Perform gradient descent (perhaps from python script), calculating the fitness of the updated genome
# at each stage to guide the ascent/descent


############################################
# For gradient descent
############################################


# Genome input used in gradient descent, output of the GA
output_directory="/home/hgjones9/spinchain/output-latest"
genome_input=$(grep "best genome:" "$output_directory/genetic.out" | cut -d':' -f2)
echo "$genome_input"

# # Define threshold to determine when to cancel the while loop based on how good the fidelity is
# threshold = 0.1

# # Fidelities of the input and output genomes
# fidelity_input = # fidelity of the input genome at a time T? 
# fidelity_output = # fidelity of the output genome at the same time T?

# # Absolute difference between input and output fidelities
# absolute_diff = $(( (fidelity_input - fidelity_output) < 0 ? -(fidelity_input - fidelity_output) : (fidelity_input - fidelity_output) ))


# while |absolute_diff > threshold:

# #   Fidelity_input_genome = calculate fidelity (at a specific time) for the input genome
# #   call gradient descent code on the input genome; output genome_optimised
# #   calculate dynamics of the output genome
# #   calculate fidelity of the output genome 

# # Genome_result = outputted genome_optimised





