import numpy as np
import matplotlib.pyplot as plt


def calculate_gradient(func, *args, h=1e-6):

    """
    This function takes an arbitrary N-dimensional function and outputs the gradient vector of that function as a numpy array.
    """
    args = np.array(args, dtype=float) # Convert arguments into a numpy array
    gradients = np.zeros_like(args) # Initialise the gradient vector
    args_plus_h = np.copy(args) # Initialise "args_plus_h" vector as a copy of "args" to be amended
    args_minus_h = np.copy(args) # Initialise "args_minus_h" vector as a copy of "args" to be amended
    
    print(args_plus_h)

    for i, arg in enumerate(args):

        args_plus_h[i] += h # Add a small increment to the i-th element in the argument array
        args_minus_h[i] -= h # Subtract a small increment to the i-th element in the argument array

        df_darg = (func(*args_plus_h) - func(*args_minus_h)) / (2 * h) # Calculate the derivative of the function wrt the i-th argument using central difference

        gradients[i] = df_darg # Add the derivative of the i-th argument to the gradient vector
    
    return gradients

def func(x, y):
    return x**2 + y**2

gradient = calculate_gradient(func, 1, 2)
print(gradient)
