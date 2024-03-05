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


cd /home/hgjones9/spinchain
pwd


# Loop over the list and run spinnet on each genome
for string in $adjusted_genomes
do
    genome=$(echo "$string" | sed "s/'//g")

    echo "bin/spinnet "<A|C>$genome""
    # Call spinnet for each genome
    bin/spinnet "<A|C>$genome"
    echo "<A|C>$genome"
done

# EVERYTHING CURRENTLY WORKS APART FROM RUNNING SPINNET ON EACH GENOME



# Calculate the fidelities of each genome by running spinnet






