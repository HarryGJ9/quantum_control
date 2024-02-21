import numpy as np

def initialize_parameters(num_params, min_val, max_val, num_samples):
    parameters = np.linspace(min_val, max_val, num_samples)
    print(parameters)
    return np.tile(parameters, (num_params, 1)).T

# Example usage:
num_params = 5         # Number of parameters
min_val = -1           # Minimum value for all parameters
max_val = 1            # Maximum value for all parameters
num_samples = 10     # Number of samples for each parameter

initialized_params = initialize_parameters(num_params, min_val, max_val, num_samples)

print("Initialized parameters:")
print(initialized_params)


