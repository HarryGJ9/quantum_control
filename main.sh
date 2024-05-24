#!/bin/bash

# User enters genome to be optimised
echo "Please enter a genome to be optimised":
read initial_genome

# User specifies whether they want initial GA optimisation or straight into gradient optimisation.
read -p "GA Optimisation? (y/n): " user_input

if [[ "$user_input" == "y" ]]; then

    # Run GA optimisation on user input genome
    /home/hgjones9/spinchain/bin/spinnet -o -G 2 "$initial_genome"

elif [[ "$user_input" == "n" ]]; then

    # Run gradient descent without user input genome
    /home/hgjones9/spinchain/bin/spinnet "$initial_genome"
fi

# Need to backup the new genome to a .txt file incase the first iteration doesn't improve
python3 /home/hgjones9/quantum_control/GA_genome.py "$user_input"
cp new_genome.txt new_genome_backup.txt

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
python3 /home/hgjones9/quantum_control/max_fidelity_time.py "$user_input"

######################
# Initialise variables
######################

# Obtain initial fidelity and infidelity at specified time
old_fidelity=$(head -n 1 /home/hgjones9/quantum_control/max_fidelity_time.txt) 
infidelity=$(echo "100 - $old_fidelity" | bc) 

echo "Initial fidelity: $old_fidelity"

# Obtain specified time for max fidelity
specified_time_old=$(tail -n +2 /home/hgjones9/quantum_control/max_fidelity_time.txt | head -n 1) 
echo "Initial time: $specified_time_old"

epsilon=0.0 # Define threshold for stopping the loop
stepsize=100 # Define gradient ascent stepsize
time_increment=0.1 # Define a time increment for temporal gradient
max_iterations=200 # Specify maximum number of iterations before gradient ascent breaks
iteration=0
echo "Iteration: $iteration"

# Initialise lists for plotting Fidelity vs iteration
iteration_lst=(0)
fidelity_lst=("$old_fidelity")

while (( $(echo "$infidelity > $epsilon" | bc -l) ))
do 

    if [ "$(echo "$iteration" == 0 | bc)" -eq 1 ]; then

        # Obtain the initial optimised output genome and make coupling adjustments
        python3 /home/hgjones9/quantum_control/initial_genome_adjuster.py "$user_input"

        # Specify output file of adjusted genomes
        output_file='/home/hgjones9/quantum_control/initial_adjusted_genomes.txt'

        # Search output.txt for the line containing the list of adjusted genomes and print them as a list
        adjusted_genomes=$(grep -oP "Adjusted genomes : \[\K.*(?=\])" "$output_file")
        # echo "Adjusted genomes: $adjusted_genomes"

        # Extract initial adjusted couplings, ready for gradient ascent
        python3 /home/hgjones9/quantum_control/extract_initial_couplings.py

        # Rename initial_couplings.txt to old_couplings.txt and backup
        mv initial_couplings.txt old_couplings.txt
        cp old_couplings.txt old_couplings_backup.txt

        # Run spinnet on each adjusted genome to calculate dynamics
        for string in $adjusted_genomes
        do
            genome=$(echo "$string" | sed "s/'\([^']*\)'.*/\1/") # Remove the individual quotation marks from each genome

            # Call spinnet for each genome, generating a different output directory for each genome
            /home/hgjones9/spinchain/bin/spinnet "@$specified_time_old$i_f$genome"
            # echo "@$specified_time_old$i_f$genome$pos_directive"
        done


        # Calculate gradient vector of the fidelity wrt couplings
        python3 /home/hgjones9/quantum_control/coupling_gradient.py 

        echo "Stepsize: $stepsize"

        # Calculate new couplings by gradient ascent
        python3 /home/hgjones9/quantum_control/update_genome.py "$stepsize"
    
        # Specify output file location of new genome
        new_genome_output='/home/hgjones9/quantum_control/new_genome.txt'  

        # Extract new genome from new_genome.txt
        new_genome=$(<"$new_genome_output")
        echo "New genome: $new_genome"

        # Run spinnet on the new genome at specified time.
        /home/hgjones9/spinchain/bin/spinnet "@$specified_time_old$i_f$new_genome$pos_directive"

        # Calculate the times
        time_minus=$(echo "$specified_time_old - $time_increment" | bc)
        # echo "$time_minus"
        time_plus=$(echo "$specified_time_old + $time_increment" | bc)

        # Run spinnet on new genome at minus a time increment and plus a time increment
        /home/hgjones9/spinchain/bin/spinnet "@${time_minus}${i_f}${new_genome}${pos_directive}"
        /home/hgjones9/spinchain/bin/spinnet "@${time_plus}${i_f}${new_genome}${pos_directive}"

        # Perform temporal gradient and obtain new fidelity and specified time
        python3 /home/hgjones9/quantum_control/fidelity_time_gradient.py 

        # # Calculate temporal gradient of udpated genome
        # python3 /home/hgjones9/quantum_control/time_gradient.py 

        # Retrieve fidelity value of most recent spinnet calculation and backup incase fidelity hasn't improved
        fidelity=$(head -n 1 /home/hgjones9/quantum_control/new_fidelity.txt) 
        cp new_fidelity.txt new_fidelity_backup.txt
        echo "Initial updated fidelity value: $fidelity"

        # Calculate infidelity using awk
        infidelity=$(awk -v f="$fidelity" 'BEGIN {printf "%.2f", 100 - f}')
        # echo "Initial updated infidelity value: $infidelity"
        
        # Retrieve new specified time and backup incase fidelity doesn't improve
        specified_time=$(head -n 1 /home/hgjones9/quantum_control/new_time.txt) 
        cp new_time.txt new_time_backup.txt
        echo "Initial updated time: $specified_time"

        # # Retrieve fidelity value of most recent spinnet calculate to initialise fidelity
        # fidelity_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out'
        # fidelity=$(awk '/fidelity/ {for (i=1; i<NF; i++) if ($i == "fidelity") {gsub(/\(/, "", $(i-1)); gsub(/%/, "", $(i-1)); print $(i-1)}}' "$fidelity_out_file")
        # echo "Initial updated fidelity value: $fidelity"

        # Append fidelity value to list
        fidelity_lst+=("$fidelity")

        # Calculate the difference between the old fidelity and new fidelity
        fidelity_diff=$(echo "$fidelity - $old_fidelity" | bc)
        echo "Fidelity difference = $fidelity_diff"

        # Increment the iteration counter
        ((iteration++))  

        echo "Iteration: $iteration"

        iteration_lst+=("$iteration")


    elif [ "$iteration" -gt 0 ]; then

        # Adjust couplings and reconstruct adjusted genomes ready for central diff
        python3 /home/hgjones9/quantum_control/genome_adjuster.py

        # Specify output file of adjusted genomes
        adjusted_genomes_out='/home/hgjones9/quantum_control/adjusted_genomes.txt'
        
        # Search output.txt for the line containing the list of adjusted genomes and print them as a list
        adjusted_genomes=$(grep -oP "Adjusted genomes : \[\K.*(?=\])" "$adjusted_genomes_out")
        # echo "Adjusted genomes: $adjusted_genomes"

        # Loop over the list of adjusted genomes and run spinnet on each genome
        for string in $adjusted_genomes
        do
            genome=$(echo "$string" | sed "s/'\([^']*\)'.*/\1/") # Remove the individual quotation marks from each genome

            # Call spinnet for each genome, generating a different output directory for each genome
            /home/hgjones9/spinchain/bin/spinnet "@$specified_time$i_f$genome$pos_directive"
            # echo "@$specified_time_old$i_f$genome$pos_directive"
        done

        # Calculate gradient vector of fidelity wrt couplings
        python3 /home/hgjones9/quantum_control/coupling_gradient.py 

        echo "Stepsize: $stepsize"

        # Calculate new couplings by gradient ascent
        python3 /home/hgjones9/quantum_control/update_genome.py "$stepsize" 

        # Run spinnet on new genome at specified time
        new_genome_output='/home/hgjones9/quantum_control/new_genome.txt'   # Specify output file location of new genome
        new_genome=$(<"$new_genome_output")  # Extract new genome from new_genome.txt
        echo "New genome: $new_genome"

        /home/hgjones9/spinchain/bin/spinnet "@$specified_time$i_f$new_genome$pos_directive"

        # Run spinnet on the new genome at specified time.
        /home/hgjones9/spinchain/bin/spinnet "@$specified_time$i_f$new_genome$pos_directive"

        # Calculate the times
        time_minus=$(echo "$specified_time - $time_increment" | bc)
        time_plus=$(echo "$specified_time + $time_increment" | bc)

        # Run spinnet on new genome at minus a time increment and plus a time increment
        /home/hgjones9/spinchain/bin/spinnet "@${time_minus}${i_f}${new_genome}${pos_directive}"
        /home/hgjones9/spinchain/bin/spinnet "@${time_plus}${i_f}${new_genome}${pos_directive}"

        # Perform temporal gradient and obtain new fidelity and specified time
        python3 /home/hgjones9/quantum_control/fidelity_time_gradient.py 

        # # Calculate temporal gradient of udpated genome
        # python3 /home/hgjones9/quantum_control/time_gradient.py "$specified_time_old"

        # Retrieve fidelity value of most recent spinnet calculation and backup incase fidelity not improved
        fidelity=$(head -n 1 /home/hgjones9/quantum_control/new_fidelity.txt) 
        cp new_fidelity.txt new_fidelity_backup.txt
        echo "Updated fidelity value: $fidelity"

        # Calculate infidelity using awk
        infidelity=$(awk -v f="$fidelity" 'BEGIN {printf "%.2f", 100 - f}')
        # echo "Updated infidelity = $infidelity"

        # Retrieve new specified time and backup incase fidelity not improved
        specified_time=$(head -n 1 /home/hgjones9/quantum_control/new_time.txt) 
        cp new_time.txt new_time_backup.txt
        echo "Updated time: $specified_time"

        # # Retrieve fidelity value from 'output_latest'
        # fidelity_out_file='/home/hgjones9/quantum_control/output-latest/genetic.out'
        # fidelity=$(awk '/fidelity/ {for (i=1; i<NF; i++) if ($i == "fidelity") {gsub(/\(/, "", $(i-1)); gsub(/%/, "", $(i-1)); print $(i-1)}}' "$fidelity_out_file")
        # echo "Updated fidelity: $fidelity"

        # Append fidelity value to fidelity_lst
        fidelity_lst+=("$fidelity")

        # Calculate the difference between the old fidelity and new fidelity
        fidelity_diff=$(echo "$fidelity - $old_fidelity" | bc)

        echo "Fidelity difference = $fidelity_diff"

        # Increment the iteration counter
        ((iteration++))  

        echo "Iteration: $iteration"

        iteration_lst+=("$iteration")

        echo "${iteration_lst[@]}"

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

        stepsize=$(echo "$stepsize * 0.5" | bc) # Halve stepsize 
        fidelity="$old_fidelity" # Revert to old fidelity (don't update fidelity)
        specified_time="$specified_time_old" # Do not update time at which fidelity is obtained
        cp new_genome_backup.txt new_genome.txt # Revert to previous genome
        cp old_couplings_backup.txt old_couplings.txt # Revert to previous couplings
        cp new_time_backup.txt new_time.txt

        echo "Fidelity not updated, sticking to previous value of: $fidelity"
        echo "Sticking to previous time: $specified_time"
        
        # Specify output file location of new genome
        genome_output='/home/hgjones9/quantum_control/new_genome.txt'

        # Extract new genome from new_genome.txt
        genome=$(<"$genome_output")
        echo "Genome not updated, sticking to previous genome: $genome"

        echo "New stepsize: $stepsize"

    # If fidelity_diff > 0, increment the stepsize slowly to still maintain growth
    elif [ "$(echo "$fidelity_diff > 0" | bc)" -eq 1 ]; then

        # Increase stepsize
        stepsize=$(echo "$stepsize * 1.5" | bc) 

        # Replace old fidelity with new fidelity
        old_fidelity="$fidelity"

        # Replace old time with new time
        specified_time_old="$specified_time"

        # Backup files
        cp new_genome.txt new_genome_backup.txt
        cp old_couplings.txt old_couplings_backup.txt
        cp new_time.txt new_time_backup.txt

        echo "Fidelity updated to: $old_fidelity"

    fi
done

# Return the minimised infidelity
echo "Optimised infidelity : $infidelity"

# Return the genome corresponding with that infidelity 
opt_genome_out="/home/hgjones9/quantum_control/output-latest/genetic.out"
opt_genome=$(awk '/stripped genome/ {print $NF}' "$opt_genome_out")

echo "Optimised Genome: $opt_genome$pos_directive"
echo "Time: $specified_time_old"

echo "${iteration_lst[@]}" > iteration_lst.txt
echo "${fidelity_lst[@]}" > fidelity_lst.txt

# Plot fidelity vs time and save
python3 /home/hgjones9/quantum_control/plotting.py