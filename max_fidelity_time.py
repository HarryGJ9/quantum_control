"""
This script obtains the maximum fidelity of the GA optimised* genome and the corresponding time. 

*Or un-optimised genome by just running the dynamics on the initial genome (for test purposes).
"""

import os
import sys

# Specify if whether GA optimisation or not
gen_alg = str(sys.argv[1])

# Obtain genome number
genome_num = str(sys.argv[2])

# genetic.out path
genetic_out_path = '/home/hgjones9/quantum_control/output_genome_' + genome_num + '/genetic.out'

# spinchain genetic.out path (FOR TESTING)
spinchain_out_path = '/home/hgjones9/spinchain/output-latest/genetic.out'


if gen_alg == "y": 

    # Open the genetic.out file to obtain the max fidelity and time of max fidelity
    with open(genetic_out_path, 'r') as file:

        # Initialise line count to track the number of lines starting with 'with fitness'
        line_count = 0
        for line in file:
            if line.startswith('with fitness'):

                # If the line starts with 'with fitness', increment the line count by 1
                line_count += 1

                # If programme reaches second line starting with 'with fitness', extract value
                if line_count == 2:

                    # Split the line into a list
                    line_split = line.split()

                    # Look for the indices of the list containing the strings 'fidelity' and 'time'
                    fidelity_idx = line_split.index('fidelity')
                    time_idx = line_split.index('time')

                    # Extract the values before 'fidelity' and after 'time'
                    fidelity_val = line_split[fidelity_idx - 1]
                    time_val = line_split[time_idx + 1]

                    # Remove '%' and '(' from fidelity_val and remove the ')' from time_val
                    fidelity_val = fidelity_val.replace('(', '').replace('%', '')
                    time_val = time_val.replace(')', '')

elif gen_alg == "n":

    # Open spinchain genetic.out file
    with open(genetic_out_path, 'r') as file: 

        # Look for line starting with 'wtih fitness'
        for line in file:
            if line.startswith('with fitness'):
            
                # Split the line into a list
                line_split = line.split()

                # Look for the indices of the list containing the strings 'fidelity' and 'time'
                fidelity_idx = line_split.index('fidelity')
                time_idx = line_split.index('time')
                
                # Extract the values before 'fidelity' and after 'time'
                fidelity_val = line_split[fidelity_idx - 1]
                time_val = line_split[time_idx + 1]

                # Remove '%' and '(' from fidelity_val and remove the ')' from time_val
                fidelity_val = fidelity_val.replace('(', '').replace('%', '')
                time_val = time_val.replace(')', '')

    
# Print values to check
# print(f'Maximum fidelity of optimised/original genome: {fidelity_val}')
# print(f'Time at maximum fidelity: {time_val}')

# Save to new files to be read in other scripts
with open('/home/hgjones9/quantum_control/max_fidelity_time_' + genome_num + '.txt', 'w') as file:
    file.write(fidelity_val + '\n')
    file.write(time_val + '\n')

