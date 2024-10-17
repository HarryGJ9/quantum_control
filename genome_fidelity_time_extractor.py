# This script opens the recently made "genetic.out" folder and extracts the five best genomes, 
# with their fidelities and corresponding times

import os

# Specify file path to output-latest
out_path = '/home/hgjones9/quantum_control/output-latest/'

# Create a list to store the results
results = []

# Open the file to read from (check if 'genetic.out' exists first)
gen_out_file = os.path.join(out_path, 'genetic.out')
if os.path.exists(gen_out_file):
    with open(gen_out_file, 'r') as file:
        lines = file.readlines()
        
        # Flag to start reading after 'FINAL SYSTEM'
        in_final_system = False
        
        # Iterate through the lines and extract data based on the 'FINAL SYSTEM' section
        for line in lines:
            line = line.strip()  # Strip any extra spaces
            
            # Check if we're in the "FINAL SYSTEM" section
            if 'FINAL SYSTEM' in line:
                in_final_system = True  # We found the section, start processing
            
            if in_final_system:
                # Check for lines containing genome information
                if 'genome' in line:
                    genome = line.split(': ')[1].strip().strip('"')
                    # print(genome)
                
                # Check for lines containing fitness, fidelity, and time information
                if 'fitness' in line:
                    parts = line.split()
                    # print(parts)
                    fidelity = float(parts[5].strip('%'))  # Fidelity is in the 6th position
                    # print(fidelity)
                    time = float(parts[-1].strip(')'))  # Time is the last element
                    # print(time)
                    results.append({'genome': genome, 'fidelity': fidelity, 'time': time})
                
                # Stop once we've extracted the top 5 genomes
                if len(results) == 5:
                    break

    # If no results were found, print a message
    if not results:
        print("No matches found in the file.")
else:
    print(f"File not found: {input_file}")

# Define output file path
output_file = '/home/hgjones9/quantum_control/extracted_genomes.txt'

# Write extracted information to a .txt file if there are results
if results:
    with open(output_file, 'w') as f:
        for result in results:
            f.write(f"{result['genome']}, {result['fidelity']}%, {result['time']}\n")
    print(f"Data successfully extracted and written to {output_file}")
else:
    print("No data to write.")
