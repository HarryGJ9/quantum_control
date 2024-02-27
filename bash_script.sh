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

output_directory="/home/hgjones9/spinchain/output-latest"
genome_input=$(grep "best genome:" "$output_directory/genetic.out" | cut -d':' -f2)
echo "$genome_input"


# threshold = threshold to determine when to cancel while loop based on how close the genome is to the final state

# while |Fidelity_input_output - Fidelity_output_genome| > threshold:

#   Fidelity_input_genome = calculate fidelity (at a specific time) for the input genome
#   call gradient descent code on the input genome; output genome_optimised
#   calculate dynamics of the output genome
#   calculate fidelity of the output genome 

# Genome_result = outputted genome_optimised





