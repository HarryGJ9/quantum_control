#!/bin/bash

########################################################
# OBTAIN ADJUSTED OUTPUT GENOMES FROM GENOME_ADJUSTER.PY
########################################################

# User enters an initial genome
echo "Please enter a genome to be optimised":
read initial_genome

# Extract initial and target state to be used later
# initial=


# Run spinnet -o on an initial genome 
/home/hgjones9/spinchain/bin/spinnet -o "$initial_genome"

# At this point, there is an output file located at /home/hgjones9/quantum_control/output_latest/genetic.out"
# This file contains the optimised genome "<i|f>AB...BC..."

# Obtain the optimised output genome and make changes using genome_adjuster.py
python3 /home/hgjones9/quantum_control/genome_adjuster.py

# Specify output file of adjusted genomes
output_file='/home/hgjones9/quantum_control/output.txt'

# Search output.txt for the line containing the list of adjusted genomes and print them as a list
adjusted_genomes=$(grep -oP "Adjusted genomes = \[\K.*(?=\])" "$output_file")

# Print the list of adjusted genomes
echo "$adjusted_genomes"

# Test on first genome
test_genome=$(echo "$adjusted_genomes" | cut -d',' -f1)

echo "$test_genome"

genome=$(echo "$string" | sed "s/^'//;s/'$//")

echo "<A|C>$genome"

cd /home/hgjones9/spinchain

pwd

# /bin/spinnet "<A|C>$test_genome"




# # Loop over the list and run spinnet on each genome
# for string in $adjusted_genomes
# do
#     genome=$(echo "$string" | tr -d "'")
#     # Call spinnet for each genome
#     /home/hgjones9/spinchain/bin/spinnet "<A|C>$genome"
#     echo "<A|C>$genome"
# done





# Calculate the fidelities of each genome by running spinnet






