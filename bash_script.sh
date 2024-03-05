#!/bin/bash

########################################################
# OBTAIN ADJUSTED OUTPUT GENOMES FROM GENOME_ADJUSTER.PY
########################################################

# User enters an initial genome
echo "Please enter a genome to be optimised":
read initial_genome


# Run spinnet -o on an initial genome 
/home/hgjones9/spinchain/bin/spinnet -o "$initial_genome"

# # Obtain the optimised output genome and make changes using genome_adjuster.py
# python3 /home/hgjones9/quantum_control/genome_adjuster.py

# # Specify output file of adjusted genomes
# output_file='/home/hgjones9/quantum_control/output.txt'

# # Search output.txt for the list of adjusted genomes, return the list
# adjusted_genomes=$(grep -oP "Adjusted genomes = \['K[^']+" "$output_file")

# # Loop over the list and run spinnet on each genome
# for genome in $adjusted_genomes
# do
#     # Call spinnet for each genome
#     /home/hgjones9/spinchain/bin/spinnet "<A|C>$genome"

# done





# Calculate the fidelities of each genome by running spinnet






