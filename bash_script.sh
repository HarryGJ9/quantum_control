#!/bin/bash

########################################################
# OBTAIN ADJUSTED OUTPUT GENOMES FROM GENOME_ADJUSTER.PY
########################################################

# User enters an initial genome
# echo "Please enter a genome to be optimised":
# read initial_genome

# Test genome: '<A|C>AB500BC500'
# initial_genome="<A|C>AB500BC500"

# # Run spinnet -o on an initial genome 
# /home/hgjones9/spinchain/bin/spinnet -o -G 5 "$initial_genome"

# /home/hgjones9/spinchain/bin/spinnet "$initial_genome"

# cd /home/hgjones9/quantum_control
# pwd

# # Specify <i|f> directive
# genetic_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out' # Path to genetic.out
# directive_line=$(grep '<i|f> directive *= *<.*>' $genetic_out_file) # Find the line containing '<i|f> directive ='
# i_f=$(echo "$directive_line" | grep -o '<[^>]*>' | tail -n 1) # Filter out <i|f> directive from the line


# echo "<Initial|Final> directive: $i_f"

# # Specify position directive
# pos_directive_line=$(grep 'pos directive *=' $genetic_out_file) # Find line containing position directive
# pos_directive=$(echo "$pos_directive_line" | sed 's/.*= *//') # Extract the string after '=' sign

# echo "Position directive: $pos_directive"

# # Retrieve max fidelity of optimised genome and time at which it occurs
# python3 /home/hgjones9/quantum_control/max_fidelity_time.py

# # Obtain the optimised output genome and make changes using genome_adjuster.py
# python3 /home/hgjones9/quantum_control/initial_genome_adjuster.py

# # Specify output file of adjusted genomes
# output_file='/home/hgjones9/quantum_control/initial_adjusted_genomes.txt'

# # Search output.txt for the line containing the list of adjusted genomes and print them as a list
# adjusted_genomes=$(grep -oP "Adjusted genomes : \[\K.*(?=\])" "$output_file")

# # # Print the list of adjusted genomes
# # echo "$adjusted_genomes"

# # #####################################################
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
#     /home/hgjones9/spinchain/bin/spinnet "$i_f$genome"
#     echo "$i_f$genome$pos_directive"
# done


# ###########################################################################
# # CALCULATE THE GRADIENT VECTOR OF THE FIDELITY WITH RESPECT TO THE COUPLINGS
# ###########################################################################

# python3 /home/hgjones9/quantum_control/calculate_gradients.py

# ############################################
# # CALCULATE NEW COUPLINGS BY GRADIENT ASCENT
# ############################################

# # # Initialise the change
# # change=0.0

# python3 /home/hgjones9/quantum_control/update_genome.py

# # Backup files
# cp old_couplings.txt old_couplings_backup.txt   # Backup the old_couplings incase fidelity doesn't improve
# cp new_genome.txt new_genome_backup.txt  # Backup the current version of new_genome.txt incase the fidelity doesn't improve


# # Update the change
# # Read the change array from the file

# # mapfile -t change < /home/hgjones9/quantum_control/change.txt
# # change=("${change[@]}")
# # echo "$change"


# ###########################
# # RUN SPINNET ON NEW GENOME
# ###########################

# # Specify output file location of new genome
# new_genome_output='/home/hgjones9/quantum_control/new_genome.txt'

# # Extract new genome from new_genome.txt
# new_genome=$(<"$new_genome_output")

# echo "New genome: $new_genome"

# /home/hgjones9/spinchain/bin/spinnet "$i_f$new_genome$pos_directive"

# # Previous generates unwanted directory, so delete
# rm -r /home/hgjones9/quantum_control/spinchain

################################
# SETUP LOOP FOR GRADIENT ASCENT
################################

# Initialise variables
# epsilon=0.01 # Threshold value for stopping optimisation
# stepsize=1000000 # Stepsize to be used in gradient ascent
# max_iterations=10 # Maximum interations before loop exits

# # Retrieve fidelity value of most recent spinnet calculate to initialise fidelity
# fidelity_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out'
# old_fidelity=$(awk '/fidelity/ {for (i=1; i<NF; i++) if ($i == "fidelity") {gsub(/\(/, "", $(i-1)); gsub(/%/, "", $(i-1)); print $(i-1)}}' "$fidelity_out_file")

# # Print the extracted fidelity value
# echo "Initial updated fidelity value: $old_fidelity"

# # Calculate infidelity using awk
# infidelity=$(awk -v f="$old_fidelity" 'BEGIN {printf "%.2f", 100 - f}')

# echo "Initial updated infidelity value: $infidelity"

######################################################################

# User enters genome to be optimised
echo "Please enter a genome to be optimised":
read initial_genome

# Run spinnet or spinnet -o 
/home/hgjones9/spinchain/bin/spinnet -o -G 5 "$initial_genome"
# /home/hgjones9/spinchain/bin/spinnet "$initial_genome"

# Need to backup the new genome to a .txt file incase the first iteration doesn't improve

# Specify <i|f> directive
genetic_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out' # Path to genetic.out
directive_line=$(grep '<i|f> directive *= *<.*>' $genetic_out_file) # Find the line containing '<i|f> directive ='
i_f=$(echo "$directive_line" | grep -o '<[^>]*>' | tail -n 1) # Filter out <i|f> directive from the line


echo "<Initial|Final> directive: $i_f"

# Specify position directive
pos_directive_line=$(grep 'pos directive *=' $genetic_out_file) # Find line containing position directive
pos_directive=$(echo "$pos_directive_line" | sed 's/.*= *//') # Extract the string after '=' sign

echo "Position directive: $pos_directive"

# Retrieve max fidelity of optimised genome and time at which it occurs
python3 /home/hgjones9/quantum_control/max_fidelity_time.py

# Initialise variables
old_fidelity=$(head -n 1 /home/hgjones9/quantum_control/max_fidelity_time.txt) # Obtain initial fidelity
echo "Initial fidelity: $old_fidelity"
infidelity=$(echo "100 - $old_fidelity" | bc) # Calculate initial infidelity
echo "Initial infidelity: $infidelity"
epsilon=0.01 # Define threshold for stopping the loop
stepsize=1000000 # Define gradient ascent stepsize
max_iterations=10 # Specify maximum number of iterations before gradient ascent breaks
iteration=0
echo "Iteration: $iteration"

while (( $(echo "$infidelity > $epsilon" | bc -l) ))
do 

    if [ "$(echo "$iteration" == 0 | bc)" -eq 1 ]; then

        # Obtain the initial optimised output genome and make coupling adjustments
        python3 /home/hgjones9/quantum_control/initial_genome_adjuster.py

        # Specify output file of adjusted genomes
        output_file='/home/hgjones9/quantum_control/initial_adjusted_genomes.txt'

        # Search output.txt for the line containing the list of adjusted genomes and print them as a list
        adjusted_genomes=$(grep -oP "Adjusted genomes : \[\K.*(?=\])" "$output_file")

        # Extract initial adjusted couplings, ready for gradient ascent
        python3 /home/hgjones9/quantum_control/extract_initial_couplings.py

        # Rename initial_couplings.txt to old_couplings.txt
        mv initial_couplings.txt old_couplings.txt

        # Run spinnet on each adjusted genome to calculate dynamics
        for string in $adjusted_genomes
        do
            genome=$(echo "$string" | sed "s/'\([^']*\)'.*/\1/") # Remove the individual quotation marks from each genome

            # Call spinnet for each genome, generating a different output directory for each genome
            /home/hgjones9/spinchain/bin/spinnet "$i_f$genome"
            echo "$i_f$genome$pos_directive"
        done


        # Calculate gradient vector of the fidelity wrt couplings
        python3 /home/hgjones9/quantum_control/calculate_gradients.py

        # Calculate new couplings by gradient ascent
        python3 /home/hgjones9/quantum_control/update_genome.py "$stepsize"

        # Backup files
        cp old_couplings.txt old_couplings_backup.txt   # Backup the old_couplings incase fidelity doesn't improve
        cp new_genome.txt new_genome_backup.txt  # Backup the current version of new_genome.txt incase the fidelity doesn't improve

        # Specify output file location of new genome
        new_genome_output='/home/hgjones9/quantum_control/new_genome.txt'  

        # Extract new genome from new_genome.txt
        new_genome=$(<"$new_genome_output")

        echo "New genome: $new_genome"

        # Run spinnet on the new genome
        /home/hgjones9/spinchain/bin/spinnet "$i_f$new_genome$pos_directive"

        # Retrieve fidelity value of most recent spinnet calculate to initialise fidelity
        fidelity_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out'
        fidelity=$(awk '/fidelity/ {for (i=1; i<NF; i++) if ($i == "fidelity") {gsub(/\(/, "", $(i-1)); gsub(/%/, "", $(i-1)); print $(i-1)}}' "$fidelity_out_file")
        echo "Initial updated fidelity value: $fidelity"

        # Calculate infidelity using awk
        infidelity=$(awk -v f="$fidelity" 'BEGIN {printf "%.2f", 100 - f}')
        echo "Initial updated infidelity value: $infidelity"

        # Calculate the difference between the old fidelity and new fidelity
        fidelity_diff=$(echo "$fidelity - $old_fidelity" | bc)

        echo "Fidelity difference = $fidelity_diff"

        # Increment the iteration counter
        ((iteration++))  

        echo "Iteration: $iteration"


    elif [ "$iteration" -gt 0 ]; then

        # Adjust couplings and reconstruct adjusted genomes ready for central diff
        python3 /home/hgjones9/quantum_control/genome_adjuster.py

        # Specify output file of adjusted genomes
        adjusted_genomes_out='/home/hgjones9/quantum_control/adjusted_genomes.txt'
        
        # Search output.txt for the line containing the list of adjusted genomes and print them as a list
        adjusted_genomes=$(grep -oP "Adjusted genomes : \[\K.*(?=\])" "$adjusted_genomes_out")

        # # Print the list of adjusted genomes
        # echo "$adjusted_genomes"

        # Loop over the list of adjusted genomes and run spinnet on each genome
        for string in $adjusted_genomes
        do
            genome=$(echo "$string" | sed "s/'\([^']*\)'.*/\1/") # Remove the individual quotation marks from each genome

            # Call spinnet for each genome, generating a different output directory for each genome
            /home/hgjones9/spinchain/bin/spinnet "$i_f$genome$pos_directive"
            echo "$i_f$genome$pos_directive"
        done

        # Calculate gradient vector of fidelity wrt couplings
        python3 /home/hgjones9/quantum_control/calculate_gradients.py
        cp gradient_latest.txt gradient_latest_backup.txt # Backup 

        # # Calculate new couplings by gradient ascent
        # python3 /home/hgjones9/quantum_control/update_genome.py "${change[@]}" "$stepsize" 

        # Calculate new couplings by gradient ascent
        python3 /home/hgjones9/quantum_control/update_genome.py "$stepsize" 

        # # Backup the current version of new_genome.txt incase the fidelity doesn't improve
        # cp new_genome.txt new_genome_backup.txt

        # # Update the change
        # change_output='/home/hgjones9/quantum_control/change.txt'
        # change=$(<"$change_output")

        # Read the change array from the file
        # mapfile -t change < /home/hgjones9/quantum_control/change.txt
        # change=("${change[@]}")
        # echo "$change"

        # Run spinnet on new genome
        new_genome_output='/home/hgjones9/quantum_control/new_genome.txt'   # Specify output file location of new genome
        new_genome=$(<"$new_genome_output")  # Extract new genome from new_genome.txt
        echo "New genome: $new_genome"
        /home/hgjones9/spinchain/bin/spinnet "$i_f$new_genome$pos_directive"

        # Retrieve fidelity value from 'output_latest'
        fidelity_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out'
        fidelity=$(awk '/fidelity/ {for (i=1; i<NF; i++) if ($i == "fidelity") {gsub(/\(/, "", $(i-1)); gsub(/%/, "", $(i-1)); print $(i-1)}}' "$fidelity_out_file")
        echo "Updated fidelity: $fidelity"
        
        # Calculate infidelity using awk
        infidelity=$(awk -v f="$fidelity" 'BEGIN {printf "%.2f", 100 - f}')
        echo "Updated infidelity = $infidelity"

        # Calculate the difference between the old fidelity and new fidelity
        fidelity_diff=$(echo "$fidelity - $old_fidelity" | bc)

        echo "Fidelity difference = $fidelity_diff"

        # Increment the iteration counter
        ((iteration++))  

        echo "Iteration: $iteration"

    fi


    #####################
    # BREAKING CONDITIONS
    #####################

    # Break the loop if the number of iterations exceeds max_iterations
     if [ $iteration -ge $max_iterations ]; then
        echo "Maximum number of iterations reached. Exiting loop."
        break
    
    # If the fidelity reaches 100%, break
    elif  [ "$(echo "$fidelity == 100" | bc)" -eq 1 ]; then
        echo "Fidelity has reached 100%. Break."
        break

    # Else if new_fidelity - old_fidelity == 0, break 
    elif [ "$(echo "$fidelity_diff == 0" | bc)" -eq 1 ]; then
        echo "Change in fidelities is zero. Break."
        break
    
    fi

    ####################
    # ADAPTIVE STEPSIZE
    ####################

    # If fidelity - old_fidelity < 0, go back to the previous genome and gradient ascend again with half the stepsize
    if [ "$(echo "$fidelity_diff < 0" | bc)" -eq 1 ]; then

        stepsize=$((stepsize / 4)) # Halve stepsize 
        fidelity="$old_fidelity" # Revert to old fidelity (don't update fidelity)
        cp new_genome_backup.txt new_genome.txt # Revert to previous genome
        cp old_couplings_backup.txt old_couplings.txt # Revert to previous couplings
        
        echo "Fidelity not updated, sticking to previous value of: $fidelity"
        echo "New stepsize: $stepsize"

        # Specify output file location of new genome
        genome_output='/home/hgjones9/quantum_control/new_genome.txt'

        # Extract new genome from new_genome.txt
        genome=$(<"$genome_output")
        echo "Genome not updated, sticking to previous genome: $genome"


    # Else, carry on and update the old fidelity with the new fidelity and backup new_genome.txt and old_couplings.txt
    else
        # Replace old fidelity with new fidelity
        old_fidelity="$fidelity"

        # Backup files
        cp new_genome.txt new_genome_backup.txt
        cp old_couplings.txt old_couplings_backup.txt

        echo "Fidelity updated to: $old_fidelity"

    fi

    echo "Stepsize: $stepsize"

done

# Return the minimised infidelity
echo "Optimised infidelity : $infidelity"

# Return the genome corresponding with that infidelity 
opt_genome_out="/home/hgjones9/quantum_control/output-latest/genetic.out"
opt_genome=$(awk '/stripped genome/ {print $NF}' "$opt_genome_out")

echo "Optimised Genome: $opt_genome$pos_directive"





    
    










