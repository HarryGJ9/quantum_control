# Start with an input genome 
# Calculate the fidelity of the genome wrt final state
# Calculate the fitness of the genome (initialises starting point)
# for a certain number of iterations:
    # calculate gradient wrt coupling 
    # if gradient ~ 0: break    
    # update the genome by current_coupling - learning_rate * gradient
    # calculate fidelity of new genome wrt final state
    # calculate fitness of new genome
    # output optimised genome, its fidelity and fitness

input_genome = 