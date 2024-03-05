#!/bin/bash

########################################################
# OBTAIN ADJUSTED OUTPUT GENOMES FROM GENOME_ADJUSTER.PY
########################################################

# Specify output file
output_file = '/home/hgjones9/quantum_control/output.txt'

# Search output.txt for the list of adjusted genomes, return the list
adjusted_genomes = $(grep -oP "Adjusted genomes = \['K[^']+" "$output_file")

# Loop over the list and run spinnet on each genome
for genome in $adjusted_genomes
do

    # Call spinnet for each genome
    /home/hgjones9/spinchain/bin/spinnet "<A|C>$genome#00"

done





# Calculate the fidelities of each genome by running spinnet






