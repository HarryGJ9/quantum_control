import subprocess
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import time


# PATHS
quant_cont_path = "/home/hgjones9/quantum_control/" # Quantum control path
spinnet_path = "/home/hgjones9/quantum_control/spinchain-ga-genetic/bin/spinnet" # Spinnet path
out_latest_path = "/home/hgjones9/quantum_control/output-latest" # Latest output path

# FUNCTIONS
def run_spinnet(args):

    """
    Run spinnet code for a genome and optional arguments e.g. ['-o', 'G', '2']

    Parameters:
        args (lst): list of arguments 
    
    Returns:
        Runs spinnet and returns output files in path "/home/hgjones9/quantum_control/output-latest"
    """
    # Run spinnet code on a genome
    result = subprocess.run([spinnet_path] + args, capture_output=True, text=True)

def parse_genome(genome):
    """
    Parse the genome string into its components: nodes, couplings, directives, and orientation.
    
    Parameters:
        genome (str): The genome string to be parsed.
    
    Returns:
        dict: A dictionary containing lists of nodes, couplings, directives, and orientation.
    """

     # Extract orientation including the '#'
    if '#' in genome:
        orientation = '#' + genome.split('#')[-1]  # Get the part after # and include '#'
    else:
        orientation = ''  # Default to empty if no orientation is found
    
    # Extract initial and final nodes
    initial_final_pattern = re.search(r'<([^|]+)\|([^>]+)>', genome)
    if initial_final_pattern:
        initial_node, final_node = initial_final_pattern.groups()
    else:
        raise ValueError("Invalid genome format: Initial and final nodes not found.")
    
    # Extract nodes and couplings
    coupling_pattern = re.findall(r'([A-Z])(\d+)', genome)  # Find pairs of (Node, Coupling)
    
    nodes = [initial_node] + [node for node, _ in coupling_pattern]
    couplings = [int(coupling) for _, coupling in coupling_pattern]
    
    # Define directives
    directives = [initial_node, final_node]
    
    return {
        'nodes': nodes,
        'couplings': couplings,
        'directives': directives,
        'orientation': orientation
    }

def construct_genome(init_dir, final_dir, nodes, couplings, orientation):
    """
    Reconstructs a genome based on the <initial|final> directives, nodes (A, B, C ...), couplings (100, 200, ...) and orientation (e.g. #00F)

    Parameters:
        init_dir (str): initial directive
        final_dir (str): final directive
        nodes (lst): list of all the nodes in the network
        couplings (lst): list of all the couplings between nodes in the network
        orientation (str): orientation directive which sets the shape of the network

    Returns: 
        genome_str (str): full reconstructed genome e.g. "<A|C>AB100BC900#00"
    """
    # Initialize the genome string with the initial and final states
    genome_parts = []
    
    # Combine nodes and couplings correctly
    for i in range(len(nodes) - 1):
        genome_parts.append(nodes[i] + nodes[i+1])  # Add the current node
        if i < len(couplings):  # Check if there is a coupling
            genome_parts.append(str(couplings[i]))  # Add coupling

    # Form the complete genome string
    genome_str = f"<{init_dir}|{final_dir}>{''.join(genome_parts)}"
    
    # Append orientation if provided
    if orientation:
        genome_str += orientation
    
    return genome_str

def extract_fidelity_time(file_path, iteration):
    """
    Extracts genome, fidelity and evaluation time from a genetic.out file.
    Can extract info all N genomes from initial genetic alg optimisation, or can extract info on just one genome in a grad ascent iteration.

    Parameters:
        file_path (str): file path containing relevant genetic.out folder.
        iteration (int): iteration of the algorithm. If iteration = 0 then this is the initial genetic alg optimisation, pre gradient ascent

    Returns:
        dict: if iteration = 0, returns a dictionary of rank, genome, max fidelity and evaluation time.
        lst: if iteration > 0, returns a list of [fidelity, evaluation time] for an evaluated genome.
    """

    if iteration == 0:
        # Read genetic.out file
        with open(file_path, 'r') as file:
            content = file.read()

        # Search for relevant lines using the previously defined regex pattern
        genome_pattern = re.compile(
            r'(\d+(?:st|nd|rd|th) best genome):\s*"([^"]+)"\s+with fitness:\s+([\d.]+)\s+\(([\d.]+)% fidelity.*time\s+([\d.]+)\)'
            )
        
        # Pattern for the first best genome
        first_best_genome_pattern = re.compile(
            r'best genome:\s*"([^"]+)"\s+with fitness:\s+([\d.]+)\s+\(([\d.]+)% fidelity.*time\s+([\d.]+)\)'
            )
        
        # Read the file and search for matches
        with open(file_path, 'r') as f:
            content = f.read()  # Read the entire file

            # Find all matches in the content
            matches = genome_pattern.findall(content)

        # Check for the first best genome
        first_best_match = first_best_genome_pattern.search(content)
        best_genomes_info = []

        # Add the first best genome if found
        if first_best_match:
            genome, fitness, fidelity, time = first_best_match.groups()
            best_genomes_info.append({
                'rank': 'best genome',  # Changed to 'best genome'
                'genome': genome,
                'fidelity': float(fidelity),
                'time': float(time)
            })

        # Append subsequent matches
        for rank, genome, fitness, fidelity, time in matches:
            best_genomes_info.append({
                'rank': rank,
                'genome': genome,
                'fidelity': float(fidelity),
                'time': float(time)
            })
        
        return best_genomes_info
        
    elif iteration >= 1:
        # Open genetic.out file and read content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Regex to find the fidelity and time in the genetic.out file
        match = re.search(r'with fitness:\s+([\d.]+)\s+\(([\d.]+)% fidelity.*time\s+([\d.]+)\)', content)

        # Find the fidelity and evaluation time in the genetic.out file
        if match:
            fidelity = float(match.group(2))
            eval_time = float(match.group(3))
        
        return [fidelity, eval_time]      

def extract_couplings(genome):
    """
    Extracts the couplings from a genome and returns them as an array of couplings.

    Parameters:
        genome (str): full genome e.g. "<A|C>AB100BC900#00"

    Returns:
        lst: list of couplings for an individual genome
    """
    genome = genome.split('#') # Split the genome by orientation directive and ignore
    
    couplings = re.findall(r'\d+', genome[0]) # Regex pattern for isolating the couplings in each genome
    return [int(coupling) for coupling in couplings] # Convert each coupling to an integer

# def normalise_couplings(couplings):
#     """
#     Takes in a list of couplings and ensures they are all of the same length, e.g. [100, 1000] -> [0100, 1000]

#     Parameters:
#         couplings (lst): list of couplings to normalise
#     Returns:
#         lst: list of normalised couplings
#     """

#     # Check if a four digit coupling is present
#     four_digit_present = any(coupling >= 1000 for coupling in couplings)

#     # Add a '0' in front of any two digit number, or change any negative numbers to 0
#     for i in range(len(couplings)):
#         if 0 < couplings[i] < 100:
#             couplings[i] = f'{couplings[i]:03d}'
#         elif couplings[i] <= 0:
#             couplings[i] = '001'

#     # If four digit coupling present, add a '0' at the start
#     if four_digit_present:
#         for i in range(len(couplings)):
#             # print(f'Coupling: {couplings[i]}')
#             # print(f'Type: {type(couplings[i])}')
#             couplings[i] = int(couplings[i])
#             if 100 <= couplings[i] < 1000:
#                 couplings[i] = f'{couplings[i]:04d}'
#             elif 0 < couplings[i] < 100:
#                 couplings[i] = f'{couplings[i]:04d}'
#             elif couplings[i] <= 0:
#                 couplings[i] = '0001'
    
    
#     return couplings

def normalise_couplings(couplings):
    """
    Takes in a list of couplings and ensures they are all of the same length, e.g. [100, 1000] -> [0100, 1000]

    Parameters:
        couplings (lst): list of couplings to normalise
    Returns:
        lst: list of normalised couplings
    """

    # Convert all couplings to integers
    couplings = [int(coupling) for coupling in couplings]

    # Check if a four-digit coupling is present
    four_digit_present = any(coupling >= 1000 for coupling in couplings)

    # Add a '0' in front of any two-digit number, or change any negative numbers to 0
    for i in range(len(couplings)):
        if 0 < couplings[i] < 100:
            couplings[i] = f'{couplings[i]:03d}'
        elif couplings[i] <= 0:
            couplings[i] = '001'

    # If four-digit coupling present, add a '0' at the start
    if four_digit_present:
        for i in range(len(couplings)):
            couplings[i] = int(couplings[i])  # Ensure integer for this check
            if 100 <= couplings[i] < 1000:
                couplings[i] = f'{couplings[i]:04d}'
            elif 0 < couplings[i] < 100:
                couplings[i] = f'{couplings[i]:04d}'
            elif couplings[i] <= 0:
                couplings[i] = '0001'

    return couplings

def perturb_couplings(couplings, h=0.1):
    """
    Perturbs each of the couplings in a list, ready for finite difference calculation.
    e.g. [100, 900] -> [110, 90, 990, 810]

    Parameters:
        couplings (lst): List of couplings to be perturbed.
    Returns:
        lst: perturbed couplings.
    """
    # Positively and negatively perturbed couplings
    perturbed_couplings_pos = [round(float(coupling) * (1 + h)) for coupling in couplings]
    perturbed_couplings_neg = [round(float(coupling) * (1 - h)) for coupling in couplings]
    # print(perturbed_couplings_pos)
    # print(perturbed_couplings_neg)

    perturbed_couplings = [val for pair in zip(perturbed_couplings_pos, perturbed_couplings_neg) for val in pair]
    # print(perturbed_couplings)

    return perturbed_couplings

def perturbed_coupling_combs(couplings, perturbed_couplings):
    """
    Calculate the different permuations of perturbed couplings e.g. if [100, 900] are the original
    couplings, then it will return: [['110', '900'], ['090', '900'], ['100', '990'], ['100', '810']]
    from which new perturbed genomes can be created.

    Parameters:
        couplings (lst): list of previous (or original) couplings
        perturbed_couplings (lst): list of perturbed couplings
    Returns:
        lst: permutations of perturbed and original couplings from which we can evaluate fidelities and 
        calculate gradient wrt couplings.
    """
    
    coupling_perms = []

    # For each original coupling, replace it with its two perturbed values
    for i in range(len(couplings)):
        # Extract the two perturbed values corresponding to this coupling
        p1, p2 = str(perturbed_couplings[2 * i]), str(perturbed_couplings[2 * i + 1])

        # Create two new coupling lists by substituting the original coupling
        for perturbed_value in [p1, p2]:
            new_couplings = [str(c) for c in couplings]  # Ensure all couplings are strings
            new_couplings[i] = perturbed_value           # Replace the specific coupling
            coupling_perms.append(new_couplings)

    return coupling_perms

def calculate_coupling_gradient(fidelities, couplings, h=0.1):

    """
    Calculates the gradient vector wrt couplings and returns as an array.

    Params: 
        fidelities (lst): list of fidelities generated from evaluating perturbed genomes.
        couplings (lst): list of un-perturbed/original couplings
        h (float): gradient stepsize
    Returns:
        arr: gradient vector wrt couplings.
    """

    # Ensure the input lists are of correct lengths
    if len(fidelities) != 2 * len(couplings):
        raise ValueError("The length of fidelities should be twice the length of couplings")

    gradient_lst = []

    # Iterate over each coupling and corresponding pair of fidelities
    for i in range(len(couplings)):
        f_plus = fidelities[2 * i]
        f_minus = fidelities[2 * i + 1]
        coupling = couplings[i]
        central_diff = (f_plus - f_minus) / (2 * h * coupling)
        gradient_lst.append(central_diff)

    # Convert list to numpy array
    gradient_arr = np.array(gradient_lst)

    return gradient_arr

def calculate_time_gradient(fidelity, genome, eval_time, iteration, h=0.5):

    # Evaluate fidelity of eval_time +/- h and extract fidelities at each time
    run_spinnet(['@' + str(eval_time + h) + genome])
    f_plus_h = new_fidelity = extract_fidelity_time(os.path.join(out_latest_path, 'genetic.out'), iteration)[0]

    run_spinnet(['@' + str(eval_time - h) + genome])
    f_minus_h = new_fidelity = extract_fidelity_time(os.path.join(out_latest_path, 'genetic.out'), iteration)[0]

    # Calculate central difference to get time gradient
    central_diff = (f_plus_h - f_minus_h) / (2 * h)

    # Convert central difference to a numpy array as our time gradient element
    time_grad = np.array(central_diff)

    return time_grad



def update_couplings(couplings, gradient, stepsize):
    """
    Adjusts the couplings based on the fidelity gradient and step size.

    Parameters:
        couplings (np.ndarray): A 1D numpy array of original couplings.
        gradient (np.ndarray): A 1D numpy array representing the gradient of the fidelities.
        stepsize (float): The step size for adjusting the couplings.

    Returns:
        np.ndarray: A 1D numpy array of adjusted couplings.
    """
    if len(couplings) != len(gradient):
        raise ValueError("The size of couplings and gradient must be the same.")

    # Adjust each coupling by adding (stepsize * gradient)
    adjusted_couplings = couplings + stepsize * gradient

    # Round the adjusted couplings to the nearest integers
    adjusted_couplings = np.round(adjusted_couplings).astype(int)

    return adjusted_couplings

def gradient_ascent(origin_genome, best_genomes, init_fidelities, eval_times, max_iterations):
    """
    Perform gradient ascent on a set of genomes.
    
    Parameters:
        origin_genome (str): The genome from which to start the optimization.
        best_genomes (list): List of best genomes to optimize.
        init_fidelities (list): List of initial fidelities corresponding to best_genomes.
        eval_times (list): List of evaluation times corresponding to best_genomes.
        max_iterations (int): The maximum number of iterations for the ascent.

    Returns:
        tuple: A tuple containing the optimized genomes, their corresponding fidelities,
               and a list of fidelity histories.
    """

    # Parse the origin genome
    parsed_genome = parse_genome(origin_genome)
    init_dir = parsed_genome['directives'][0]
    final_dir = parsed_genome['directives'][1]
    nodes = parsed_genome['nodes']
    origin_couplings = parsed_genome['couplings']
    orientation = parsed_genome['orientation']

    # Store optimized genomes and fidelities
    optimized_genomes = best_genomes[:]  # Start with the best genomes
    optimized_fidelities = init_fidelities[:]  # Start with the initial fidelities

    # Initialize a list to track fidelity history for each genome
    fidelity_history = [[] for _ in range(len(optimized_genomes))]

    # Perform gradient ascent for each genome
    for index, genome in enumerate(optimized_genomes):
        print(f"Optimizing genome {index + 1}/{len(optimized_genomes)}")
        current_eval_time = eval_times[index]
        print(f"Evaluation time: {current_eval_time}")

        # Initialize step size for this genome
        stepsize = 20000 

        for iteration in range(1, max_iterations + 1):  # Start from 1
            print(f"Iteration: {iteration}")

            # Extract couplings and perturb them
            init_couplings = extract_couplings(genome)
            # print(f"Initial couplings: {init_couplings}")
            perturbed_couplings = perturb_couplings(init_couplings)
            perturbed_couplings_combs = perturbed_coupling_combs(init_couplings, perturbed_couplings)
            # norm_perturbed_couplings = normalise_couplings(perturbed_coupling_combs)
            norm_perturbed_couplings = [normalise_couplings(comb) for comb in perturbed_couplings_combs]
            # print(f"Perturbed Couplings: {norm_perturbed_couplings}")

            # Construct perturbed genomes
            # perturbed_genomes = construct_genome(init_dir,final_dir, nodes, norm_perturbed_couplings, orientation)
            perturbed_genomes = [construct_genome(init_dir, final_dir, nodes, nc, orientation) for nc in norm_perturbed_couplings]
            # print(f"Perturbed Genomes: {perturbed_genomes}")

            # Evaluate the fidelities of perturbed genomes
            fidelities = []
            for pert_genome in perturbed_genomes:
                # print(f"Perturbed Genome Type: {type(pert_genome)}")
                # print(f"Perturbed Genome: {pert_genome}")
                
                # Track the modification time of the specific file before running spinnet
                genetic_out_path = os.path.join(out_latest_path, 'genetic.out')
                if os.path.exists(genetic_out_path):
                    prev_mod_time = os.path.getmtime(genetic_out_path)
                    # print(f"Previous Modification Time: {prev_mod_time}")
                else:
                    print(f"{genetic_out_path} does not exist yet.")
                    prev_mod_time = None  # If file doesn't exist, set to None

                # Run spinnet
                run_spinnet(['@' + str(current_eval_time) + pert_genome])
                # print(f"Ran spinnet with genome: {pert_genome} and eval time: {current_eval_time}")

                # Wait for the 'genetic.out' file to be updated or newly created
                timeout = 30  # Maximum wait time in seconds
                start_time = time.time()

                while True:
                    if os.path.exists(genetic_out_path):
                        new_mod_time = os.path.getmtime(genetic_out_path)
                        # print(f"New Modification Time: {new_mod_time}")
                        if prev_mod_time is None or new_mod_time > prev_mod_time:
                            # print("File has been updated.")
                            break  # New file created or updated
                    if time.time() - start_time >= timeout:
                        print(f"Timeout: File {genetic_out_path} was not updated within {timeout} seconds.")
                        # Instead of returning, handle the timeout gracefully by skipping this genome
                        fidelity_history[index].append(None)  # Mark this as None for this iteration
                        break  # Exit the waiting loop and continue
                    time.sleep(1)  # Wait 1 second before checking again
                fidelity = extract_fidelity_time(os.path.join(out_latest_path, 'genetic.out'), iteration)[0]
                fidelities.append(fidelity)
            print(f"Fidelities of perturbed genomes: {fidelities}")

            # Calculate gradient
            gradient = calculate_coupling_gradient(fidelities, init_couplings)
            print(f"Gradient: {gradient}")

            # Update couplings
            new_couplings = update_couplings(init_couplings, gradient, stepsize=stepsize)
            # print(f"Updated couplings: {new_couplings}")

            # Construct the new optimized genome
            new_optimized_genome = construct_genome(init_dir, final_dir, nodes, new_couplings, orientation)
            print(f"New optimised genome: {new_optimized_genome}")
            run_spinnet(['@' + str(current_eval_time) + new_optimized_genome])
            new_fidelity_1 = extract_fidelity_time(os.path.join(out_latest_path, 'genetic.out'), iteration)[0]
            print(f"Updated fidelity: {new_fidelity_1}")

            # Obtain time gradient element
            time_grad = calculate_time_gradient(new_optimized_genome, current_eval_time, iteration)
            print(f"Time gradient: {time_grad}")

            # Obtain new evaluation time based on time gradient
            new_eval_time = current_eval_time + time_grad
            print(f"New evaluation time: {new_eval_time}")

            # Obtain fidelity of new genome with new eval time
            run_spinnet(['@' + str(new_eval_time) + new_optimized_genome])
            new_fidelity_2 = new_fidelity = extract_fidelity_time(os.path.join(out_latest_path, 'genetic.out'), iteration)[0]
            print(f"Fidelity with new eval time: {new_fidelity_2}")

            if new_fidelity_2 > new_fidelity_1:
                print(f"Fidelity improved with updated eval time.")
                current_eval_time = new_eval_time
                new_fidelity = new_fidelity_2
                print(current_eval_time)
            elif new_fidelity_2 <= new_fidelity_1:
                print(f"Fidelity unchanged by updated eval time. Stick to {current_eval_time}")
                current_eval_time = current_eval_time
                new_fidelity = new_fidelity_1

            # Record the fidelity
            fidelity_history[index].append(new_fidelity)

            # Check if the new fidelity is 100
            if new_fidelity == 100:
                print("Fidelity = 100. Stopping optimization for this genome.")
                break
            elif new_fidelity == fidelity_history[index - 1] and fidelity_history[index - 2]:
                print("Fidelities have remained constant three times in a row. Break")
                break
            elif new_fidelity > optimized_fidelities[index]:
                print("Fidelity improved.")
                optimized_genomes[index] = new_optimized_genome  # Update the genome
                optimized_fidelities[index] = new_fidelity  # Update the fidelity
                genome = new_optimized_genome
                stepsize *= 1.2  # Increase step size if the fidelity improved
                print(stepsize)
            elif new_fidelity < optimized_fidelities[index]:
                # If not better, retain the previous genome and fidelity
                print(f"Fidelity not improved. Reverting to {genome}")
                genome = genome
                stepsize *= 0.5  # Reduce step size if fidelity goes down
                print(stepsize)
            

            # If the stepsize decreases below 10, break.
            if stepsize <= 10:
                print("Stepsize too low. Break.")
                optimized_genomes[index] = new_optimized_genome
                break

    return optimized_genomes, optimized_fidelities, fidelity_history

def plot_fidelity_history(fidelity_history, max_iterations):
    """
    Plot the fidelity history for each genome.

    Parameters:
        fidelity_history (list): A list of lists containing the fidelity history for each genome.
        max_iterations (int): The maximum number of iterations for the ascent.
    """
    plt.figure(figsize=(10, 6))

    # Create a line for each genome's fidelity history
    for index, fidelities in enumerate(fidelity_history):
        plt.plot(range(1, len(fidelities) + 1), fidelities, label=f'Genome {index + 1}', marker='o')

    plt.title('Fidelity of Each Genome Over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Fidelity')
    plt.ylim(np.min(fidelities), 100)  # Assuming fidelity is between 0 and 100
    plt.xlim(1, max_iterations)  # Based on the number of iterations
    plt.legend()
    plt.grid()
    plt.show()

def gradient_ascent_single(args):
    origin_genome, genome, current_eval_time, iteration, out_latest_path = args
    
    # Run spinnet
    run_spinnet([f'@{current_eval_time}', genome])
    
    # Wait for the output file to be created
    file_path = os.path.join(out_latest_path, 'genetic.out')
    for _ in range(10):  # Retry up to 10 times
        if os.path.exists(file_path):
            break
        print(f"File not found: {file_path}. Retrying...")
        time.sleep(1)  # Wait before retrying

    # Now try to read the fidelity
    fidelity, eval_time = extract_fidelity_time(file_path, iteration)
    
    # Ensure fidelity is not None before proceeding
    if fidelity is None:
        print("Fidelity could not be retrieved; exiting this genome's optimization.")
        return None  # Or handle appropriately

def gradient_ascent_parallel(origin_genome, best_genomes, init_fidelities, eval_times, max_iterations, out_latest_path):
    inputs = []
    for genome, eval_time in zip(best_genomes, eval_times):
        # Assuming 'iteration' is some constant value or can be initialized here
        for iteration in range(max_iterations):  # Adjust this based on your needs
            inputs.append((origin_genome, genome, eval_time, iteration, out_latest_path))

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(gradient_ascent_single, inputs)
    
    # Assuming results is structured correctly
    return list(zip(*results))  # Adjust this if results are structured differently

# def plot_fidelity_history(fidelity_history, max_iterations):
#     """
#     Plot the fidelity history for each genome.

#     Parameters:
#         fidelity_history (list): A list of lists containing the fidelity history for each genome.
#         max_iterations (int): The maximum number of iterations for the ascent.
#     """
#     plt.figure(figsize=(10, 6))

#     # Create a line for each genome's fidelity history
#     for index, fidelities in enumerate(fidelity_history):
#         plt.plot(range(1, len(fidelities) + 1), fidelities, label=f'Genome {index + 1}', marker='o')

#     plt.title('Fidelity of Each Genome Over Iterations')
#     plt.xlabel('Iteration')
#     plt.ylabel('Fidelity')
#     plt.ylim(0, 100)  # Assuming fidelity is between 0 and 100
#     plt.xlim(1, max_iterations)  # Based on the number of iterations
#     plt.axhline(y=100, color='r', linestyle='--', label='Fidelity = 100')
#     plt.legend()
#     plt.grid()
#     plt.show()


#########
# TESTING
#########

# Test genome
genome_full = "<A|G>AB5000BC5000CD5000DE5000EF5000FG5000#000000"


# Run spinnet with optimisation PASSED
run_spinnet(['-o', '-G', '2', genome_full])

# Extract top 5 genomes, fidelities and evaluation times
best_genome_info = extract_fidelity_time(os.path.join(out_latest_path, 'genetic.out'), 0)


# Extract genomes, fidelities, and times into separate lists
part_opt_genomes = [entry['genome'] for entry in best_genome_info]
print(f"Top 5 genomes: {part_opt_genomes}")
init_fidelities = [entry['fidelity'] for entry in best_genome_info]
print(f"Top 5 genome fidelities: {init_fidelities}")
eval_times = [entry['time'] for entry in best_genome_info]
print(f"Top 5 genome evaluation times: {eval_times}")

max_iterations = 10
optimised_genomes, optimised_fidelities, fidelity_history = gradient_ascent(genome_full, part_opt_genomes, init_fidelities, eval_times, max_iterations)
print(f"Optimised genomes and fidelities: {optimised_genomes}, {optimised_fidelities}")

plot_fidelity_history(fidelity_history, max_iterations)


# # Usage
# optimized_genomes, optimized_fidelities, fidelity_histories = gradient_ascent_parallel(genome_full, part_opt_genomes, init_fidelities, eval_times, max_iterations, out_latest_path)
# plot_fidelity_history(fidelity_histories, max_iterations)

##########################################################################################################################################
# STEP 0:
# User inputs the genome and it is picked apart to provide a list of nodes, coupling strengths, <initial|final> directives and network orientation
##########################################################################################################################################

# # # User inputs a genome
# # genome_full = input("Input a genome:")

# # For now, test only on <A|C>AB100BC900#00
# genome_full = "<A|C>AB100BC900#00"


# parsed_genome = parse_genome(genome_full)
# # print(parsed_genome)
# nodes = parsed_genome['nodes']
# print(nodes)
# initial_couplings = parsed_genome['couplings']
# print(initial_couplings)
# directives = parsed_genome['directives']
# print(directives)
# orientation = parsed_genome['orientation']
# print(orientation)
# initial_directive = nodes[0]
# final_directive = nodes[1]

# # #####################
# # # STEP 1:
# # # Run modified gen alg and obtain top 5 genomes, max fidelities and corresponding times
# # #####################


# # Obtain the 5 optimised genomes, their maximum fidelities and corresponding times


# #########################
# # # STEP 2: Extract couplings
# #########################

# # Function for extracting couplings of each genome


# # Create a list of lists for the couplings of each genome
# couplings_arr = np.array([extract_couplings(genome['genome']) for genome in best_genomes_info])
# print("Couplings array: ", couplings_arr)

# ##########################
# #STEP 3: Gradient ascent
# ##########################


# # run_spinnet(genome)

# # # run_spinnet("<A|C>AB100BC900")


# def coupling_grad(couplings):
#     """
#     Calculate the gradient using the finite difference method.
    
#     Parameters:
#         couplings (np.array): Current coupling values.
#         perturbation (float): Amount to perturb the couplings.
#         fidelity (float): Current fidelity value.
    
#     Returns:
#         np.array: Gradient of fidelity with respect to couplings.
#     """
#     gradient = np.zeros_like(couplings, dtype=float)
    
#     for i in range(len(couplings)):
#         # Perturb positively
#         perturbed_couplings_pos = couplings.copy()
#         perturbed_couplings_pos[i] += 0.1 * couplings[i]
#         genome_pos = construct_genome(perturbed_couplings_pos)
#         output_pos = run_spinnet(genome_pos)
#         fidelity_pos, _ = extract_fidelity_time(output_pos)

#         # Perturb negatively
#         perturbed_couplings_neg = couplings.copy()
#         perturbed_couplings_neg[i] -= 0.1 * couplings[i]
#         genome_neg = construct_genome(perturbed_couplings_neg)
#         output_neg = run_spinnet(genome_neg)
#         fidelity_neg, _ = extract_fidelity_time(output_neg)

#         # Calculate the gradient
#         gradient[i] = (fidelity_pos - fidelity_neg) / (2 * np.mean(couplings))
    
#     return gradient

# grad = coupling_grad(initial_couplings)
# print(grad)

# # Define parameters for gradient ascent
# max_iterations = 10 # Maximum number of gradient ascent iterations
# perturbation_frac = 0.1 # Amount to perturb couplings for finite difference calculation
# stepsize = 0.1 # Gradient ascent stepsize

# # # def grad_ascent(couplings_arr, fidelities):

# # #     # Find how many genomes there are
# # #     num_genomes = couplings_arr.shape[0]

# # #     # Iterate over max_iterations
# # #     for iteration in range(MAX_ITERATIONS):
# # #         print(f"\nIteration: {iteration + 1}")

# # #         # Iterate over each genome
# # #         for i in range(num_genomes):
# # #             original_couplings = couplings_arr[i].copy
# # #             initial_fidelity = fidelities[i]

# # #             # Perturb couplings 






