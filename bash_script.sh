#!/bin/bash

########################################################
# OBTAIN ADJUSTED OUTPUT GENOMES FROM GENOME_ADJUSTER.PY
########################################################

# User enters an initial genome
echo "Please enter a genome to be optimised":
read initial_genome

# Extract initial and target state to be used later
# initial=initial_site
# final=final_site

# Run spinnet -o on an initial genome 
/home/hgjones9/spinchain/bin/spinnet -o "$initial_genome"

# At this point, there is an output file located at /home/hgjones9/quantum_control/output_latest/genetic.out"
# This file contains the optimised genome "<i|f>AB...BC..."

cd /home/hgjones9/quantum_control
pwd

# Obtain the optimised output genome and make changes using genome_adjuster.py
python3 /home/hgjones9/quantum_control/genome_adjuster.py

# Specify output file of adjusted genomes
output_file='/home/hgjones9/quantum_control/initial_adjusted_genomes.txt'

# Search output.txt for the line containing the list of adjusted genomes and print them as a list
adjusted_genomes=$(grep -oP "Adjusted genomes = \[\K.*(?=\])" "$output_file")

# Print the list of adjusted genomes
echo "$adjusted_genomes"

#####################################################
# OBTAIN INITIAL COUPLINGS, READY FOR GRADIENT ASCENT
#####################################################

python3 extract_initial_couplings.py

#######################################################################
# RENAME 'initial_couplings.txt' TO 'old_couplings.txt' FOR GRAD ASCENT
#######################################################################

mv initial_couplings.txt old_couplings.txt


##################################################
# RUN SPINNET ON EACH GENOME TO CALCUALTE DYNAMICS
##################################################

# Loop over the list of adjusted genoms and run spinnet on each genome
for string in $adjusted_genomes
do
    genome=$(echo "$string" | sed "s/'\([^']*\)'.*/\1/") # Remove the individual quotation marks from each genome

    # Call spinnet for each genome, generating a different output directory for each genome
    /home/hgjones9/spinchain/bin/spinnet "<A|C>$genome"
    echo "<A|C>$genome"
done


###########################################################################
# CALCULATE THE GRADIENT VECTOR OF THE FIDELITY WITH RESPECT TO THE GENOMES
###########################################################################

python3 /home/hgjones9/quantum_control/calculate_gradients.py


########################################################################################################
# EXTRACT GA OPTIMISED COUPLINGS FROM 'initial_adjusted_genomes.txt' AND SAVE TO 'old_couplings.txt'
########################################################################################################



############################################
# CALCULATE NEW COUPLINGS BY GRADIENT ASCENT
############################################

python3 /home/hgjones9/quantum_control/update_genome.py









