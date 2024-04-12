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

# Test genome: '<A|C>AB500BC500'
# initial_genome="<A|C>AB500BC500"

# Run spinnet -o on an initial genome 
/home/hgjones9/spinchain/bin/spinnet -o "$initial_genome"

cd /home/hgjones9/quantum_control
pwd

# Specify <i|f> directive
genetic_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out' # Path to genetic.out
directive_line=$(grep '<i|f> directive *= *<.*>' $genetic_out_file) # Find the line containing '<i|f> directive ='
i_f=$("$directive_line" | grep -o '<[^>]*>') # Filter out <i|f> directive from the line

echo "$i_f"

# # Retrieve max fidelity of optimised genome and time at which it occurs
# python3 /home/hgjones9/quantum_control/max_fidelity_time.py


# # At this point, there is an output file located at /home/hgjones9/quantum_control/output_latest/genetic.out"
# # This file contains the optimised genome "<i|f>AB...BC..."


# # Obtain the optimised output genome and make changes using genome_adjuster.py
# python3 /home/hgjones9/quantum_control/initial_genome_adjuster.py

# # Specify output file of adjusted genomes
# output_file='/home/hgjones9/quantum_control/initial_adjusted_genomes.txt'

# # Search output.txt for the line containing the list of adjusted genomes and print them as a list
# adjusted_genomes=$(grep -oP "Adjusted genomes : \[\K.*(?=\])" "$output_file")

# # Print the list of adjusted genomes
# echo "$adjusted_genomes"

# #####################################################
# # OBTAIN INITIAL COUPLINGS, READY FOR GRADIENT ASCENT
# #####################################################

# python3 /home/hgjones9/quantum_control/extract_initial_couplings.py

# #######################################################################
# # RENAME 'initial_couplings.txt' TO 'old_couplings.txt' FOR GRAD ASCENT
# #######################################################################

# mv initial_couplings.txt old_couplings.txt

# ##################################################
# # RUN SPINNET ON EACH GENOME TO CALCUALTE DYNAMICS
# ##################################################

# # Loop over the list of adjusted genomes and run spinnet on each genome
# for string in $adjusted_genomes
# do
#     genome=$(echo "$string" | sed "s/'\([^']*\)'.*/\1/") # Remove the individual quotation marks from each genome

#     # Call spinnet for each genome, generating a different output directory for each genome
#     /home/hgjones9/spinchain/bin/spinnet "<A|C>$genome"
#     echo "<A|C>$genome"
# done


# ###########################################################################
# # CALCULATE THE GRADIENT VECTOR OF THE FIDELITY WITH RESPECT TO THE GENOMES
# ###########################################################################

# python3 /home/hgjones9/quantum_control/calculate_gradients.py

# ############################################
# # CALCULATE NEW COUPLINGS BY GRADIENT ASCENT
# ############################################

# python3 /home/hgjones9/quantum_control/update_genome.py

# ###########################
# # RUN SPINNET ON NEW GENOME
# ###########################

# # Specify output file location of new genome
# new_genome_output='/home/hgjones9/quantum_control/new_genome.txt'

# # Extract new genome from new_genome.txt
# new_genome=$(<"$new_genome_output")

# /home/hgjones9/spinchain/bin/spinnet "<A|C>$new_genome"

# ################################
# # SETUP LOOP FOR GRADIENT ASCENT
# ################################

# # Define threshold value for stopping the optimisation
# epsilon=0.01

# # Retrieve fidelity value of most recent spinnet calculate to initialise fidelity
# fidelity_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out'
# fidelity=$(awk '/fidelity/ {for (i=1; i<NF; i++) if ($i == "fidelity") {gsub(/\(/, "", $(i-1)); gsub(/%/, "", $(i-1)); print $(i-1)}}' "$fidelity_out_file")

# # Print the extracted fidelity value
# echo "$fidelity"

# # Calculate infidelity using awk
# infidelity=$(awk -v f="$fidelity" 'BEGIN {printf "%.2f", 100 - f}')

# echo "$infidelity"

# # Initialise number of iterations
# max_iterations=5
# iteration=0
# while (( $(echo "$infidelity > $epsilon" | bc -l) ))
# do  

#     # echo "Infidelity: $infidelity"
#     # echo "Epsilon: $epsilon"
#     # echo "Comparison: $(echo "$infidelity > $epsilon" | bc -l)"

#     # Break the loop if the number of iterations 
#      if [ $iteration -ge $max_iterations ]; then
#         echo "Maximum number of iterations reached. Exiting loop."
#         break
#     fi

#     # Adjust couplings and reconstruct adjusted genomes ready for central diff
#     python3 /home/hgjones9/quantum_control/genome_adjuster.py

#     # Specify output file of adjusted genomes
#     adjusted_genomes_out='/home/hgjones9/quantum_control/adjusted_genomes.txt'
    
#     # Search output.txt for the line containing the list of adjusted genomes and print them as a list
#     adjusted_genomes=$(grep -oP "Adjusted genomes : \[\K.*(?=\])" "$adjusted_genomes_out")

#     # Print the list of adjusted genomes
#     echo "$adjusted_genomes"

#     # Loop over the list of adjusted genomes and run spinnet on each genome
#     for string in $adjusted_genomes
#     do
#         genome=$(echo "$string" | sed "s/'\([^']*\)'.*/\1/") # Remove the individual quotation marks from each genome

#         # Call spinnet for each genome, generating a different output directory for each genome
#         /home/hgjones9/spinchain/bin/spinnet "<A|C>$genome"
#         echo "<A|C>$genome"
#     done

#     # Calculate gradient vector of fidelity wrt couplings
#     python3 /home/hgjones9/quantum_control/calculate_gradients.py

#     # Calculat new couplings by gradient ascent
#     python3 /home/hgjones9/quantum_control/update_genome.py

#     # Run spinnet on new genome
#     # Specify output file location of new genome
#     new_genome_output='/home/hgjones9/quantum_control/new_genome.txt'

#     # Extract new genome from new_genome.txt
#     new_genome=$(<"$new_genome_output")

#     /home/hgjones9/spinchain/bin/spinnet "<A|C>$new_genome"

#     # Retrieve fidelity value from 'output_latest'
#     fidelity_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out'
#     fidelity=$(awk '/fidelity/ {for (i=1; i<NF; i++) if ($i == "fidelity") {gsub(/\(/, "", $(i-1)); gsub(/%/, "", $(i-1)); print $(i-1)}}' "$fidelity_out_file")

#     # Print the extracted fidelity value
#     echo "$fidelity"

#     # Calculate infidelity using awk
#     infidelity=$(awk -v f="$fidelity" 'BEGIN {printf "%.2f", 100 - f}')

#     echo "$infidelity"

#     # Increment the iteration counter
#     ((iteration++))  

#     echo "$iteration"

# done

# # Return the minimised infidelity
# echo "Optimised infidelity : $infidelity"

# # Return the genome corresponding with that infidelity 
# opt_genome_out="/home/hgjones9/quantum_control/output-latest/genetic.out"
# opt_genome=$(awk '/stripped genome/ {print $NF}' "$opt_genome_out")

# echo "Stripped Genome: $opt_genome"





    
    










