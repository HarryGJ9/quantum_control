import subprocess
import re
import os
import numpy as np


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

def normalise_couplings(couplings):
    """
    Takes in a list of couplings and ensures they are all of the same length, e.g. [100, 1000] -> [0100, 1000]

    Parameters:
        couplings (lst): list of couplings to normalise
    Returns:
        lst: list of normalised couplings
    """

    # Check if a four digit coupling is present
    four_digit_present = any(coupling >= 1000 for coupling in couplings)

    # Add a '0' in front of any two digit number, or change any negative numbers to 0
    for i in range(len(couplings)):
        if 0 < couplings[i] < 100:
            couplings[i] = f'{couplings[i]:03d}'
        elif couplings[i] <= 0:
            couplings[i] = '001'

    # If four digit coupling present, add a '0' at the start
    if four_digit_present:
        for i in range(len(couplings)):
            # print(f'Coupling: {couplings[i]}')
            # print(f'Type: {type(couplings[i])}')
            couplings[i] = int(couplings[i])
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

def calculate_gradient(fidelities, couplings, h=0.1):

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

def gradient_ascent(origin_genome, init_genomes, init_fidelities, eval_times, max_iterations):

    parsed_genome = parse_genome(origin_genome)
    init_dir = parsed_genome['directives'][0]
    final_dir = parsed_genome['directives'][1]
    nodes = parsed_genome['nodes']
    init_couplings = parsed_genome['couplings']
    orientation = parsed_genome['orientation']
    
    for i in range(max_iterations):
        for genome in init_genomes:
            init_couplings = extract_couplings(genome)
            perturbed_couplings = perturb_couplings(init_couplings, h=0.1)
            perturbed_couplings = perturbed_coupling_combs(init_couplings, perturbed_couplings)
            norm_perturbed_couplings = normalise_couplings(perturbed_couplings)

            perturbed_genomes = construct_genome(init_dir, final_dir, nodes, norm_perturbed_couplings, orientation)

            run_spinnet()






#########
# TESTING
#########

# Test genome
genome_full = "<A|C>AB100BC900#00"

# # Run spinnet with optimisation PASSED
# run_spinnet(['-o', '-G', '2', genome_full])

# # Run spinnet without optimisation PASSED
# run_spinnet([genome_full])

# # Parse genome PASSED
# print(parse_genome(genome_full))

# # Construct genome given parsed genome PASSED
# print(construct_genome('A', 'D', ['A', 'B', 'C', 'D'], ['100', '900', '800'], ''))

# # Extract 1-5 ranked genomes, their fidelities and evaluation times from the gen alg PASSED
# print(extract_fidelity_time(os.path.join(out_latest_path, "genetic.out"), iteration=0))

# # Extract fidelity and evaluation time from a singular evaluated genome PASSED
# print(extract_fidelity_time(os.path.join(out_latest_path, "genetic.out"), iteration=1))

# Extract couplings from a genome and present as a list PASSED
couplings = extract_couplings(genome_full)
print(extract_couplings(genome_full))

# Normalise all the couplings to reconstruct any genome with any arbitrary couplings PASSED
norm_couplings = normalise_couplings(couplings)
# print(norm_couplings)

# Perturb couplings PASSED
perturbed_couplings = perturb_couplings(couplings)
print(perturbed_couplings)

# Normalise perturbed couplings PASSED
norm_perturbed_couplings = normalise_couplings(perturbed_couplings)
print(norm_perturbed_couplings)

# Reconstruct genomes based off of perturbed couplings PASSED
perturbed_couplings = perturbed_coupling_combs(norm_couplings, norm_perturbed_couplings)
print(perturbed_couplings)


# Use the original construct_genome function to generate genomes
perturbed_genomes = [
    construct_genome('A', 'C', ['A', 'B', 'C'], couplings, "#00")
    for couplings in perturbed_couplings
]

print(perturbed_genomes)

# For each perturbed genome, run spinnet @ evaluation time and fetch result
fidelities = []
for genome in perturbed_genomes:
    print(genome)
    run_spinnet(['15.80', genome])
    fidelity = extract_fidelity_time(os.path.join(out_latest_path, 'genetic.out'), iteration=1)[0]
    fidelities.append(fidelity)
    fidelities_arr = np.array(fidelities)
print(fidelities)

# Test to see if we can calculate gradient vector of fidelities wrt couplings
grad_vector = calculate_gradient(fidelities_arr, couplings)
print(grad_vector)

# Test to see if we can update the couplings
updated_couplings = update_couplings(couplings, grad_vector, 100)
print(updated_couplings)

# Reconstruct new genome
updated_genome = construct_genome('A', 'C', ['A', 'B', 'C'], updated_couplings, '#00')
print(updated_genome)

# Evaluate fidelity of new genome and repeat whole process until we converge on a fidelity ~ 100%!

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






