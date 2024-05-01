import os

# Get maximum fidelity and the time of max fidelity from the first genetic.out file

# genetic.out path
genetic_out_path = '/home/hgjones9/quantum_control/output-latest/genetic.out'

with open(genetic_out_path, 'r') as file:

    # Initialise line count to track the number of lines starting with 'with fitness'
    line_count = 0
    for line in file:
        if line.startswith('with fitness'):
            # If the line starts with 'with fitness', increment the line count by 1
            line_count += 1
            if line_count == 2:
                # If it is the second line starting with 'with fitness', split the line into a list
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
    
    # # TESTING WITHOUT GA
    # for line in file:
    #     if line.startswith('with fitness'):
        
    #         # If line starts with 'with fitness', split the line into a list
    #         line_split = line.split()
    #         # Look for the indices of the list containing the strings 'fidelity' and 'time'
    #         fidelity_idx = line_split.index('fidelity')
    #         time_idx = line_split.index('time')
    #         # Extract the values before 'fidelity' and after 'time'
    #         fidelity_val = line_split[fidelity_idx - 1]
    #         time_val = line_split[time_idx + 1]

    #         # Remove '%' and '(' from fidelity_val and remove the ')' from time_val
    #         fidelity_val = fidelity_val.replace('(', '').replace('%', '')
    #         time_val = time_val.replace(')', '')

    
    # Print values to check
    print(f'Maximum fidelity of GA optimised genome: {fidelity_val}')
    print(f'Time at maximum fidelity: {time_val}')

# Save to new files to be read in other scripts
with open('/home/hgjones9/quantum_control/max_fidelity_time.txt', 'w') as file:
    file.write(fidelity_val + '\n')
    file.write(time_val + '\n')

