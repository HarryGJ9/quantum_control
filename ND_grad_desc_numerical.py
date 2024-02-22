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
    
    # print(args_plus_h)

    for i, arg in enumerate(args):

        args_plus_h[i] += h # Add a small increment to the i-th element in the argument array
        args_minus_h[i] -= h # Subtract a small increment to the i-th element in the argument array

        df_darg = (func(*args_plus_h) - func(*args_minus_h)) / (2 * h) # Calculate the derivative of the function wrt the i-th argument using central difference

        gradients[i] = df_darg # Add the derivative of the i-th argument to the gradient vector
    
    return gradients



# gradient = calculate_gradient(func, 1, 2)
# print(gradient)

def gradient_descent(func, num_args, min_val, max_val, max_iterations=1000, learning_rate=0.001):


    # Initialise parameter values e.g. x, y, ... values
    
    # args = np.array(args, dtype=float) # Convert arguments into a numpy array
    # num_args = np.size(args) # Number of arguments in the function
    param_vals = np.arange(min_val, max_val, 0.1) # Array of values for each parameter
    arg_vals = np.tile(param_vals, (num_args,1)) # Construct a 2D array with each column containing the parameter values for each argument

    print(f"Initial values to be passed into function are: {arg_vals}")

    ################
    # SO FAR, FUNCTION IS ABLE TO PRINT OUT AN N X M ARRAY OF PARAMETER VALUES 
    # N = NUMBER OF ROWS : SPECIFIES VALUES OF EACH PARAMETER THAT DEFINE THE PLANE
    # M = NUMBER OF COLUMNS : SPECIFIES HOW MANY PARAMETERS IN THE FUNCTION
    # E.G. FOR N = 2, (X, Y) AND M = (-1, 1, 0.1) SPECIFIES A 3D GRID WITH 
    # X & Y VALUES GOING FROM -1 TO 1 WIHT 0.1 STEP SIZE
    # FROM HERE WE CAN PLUG VALUES INTO A FUNCTION WHICH DEFINES THE LANDSCAPE
    ###############
    

    # initialise function values e.g. f(x,y, ...) values that generate landscape
    func_vals = func(*arg_vals)
    print(f"Landscape values: {func_vals}")

    # initialise position e.g. current_pos = (x_position, y_position, ...)
    initial_parameter_vals = np.random.uniform(min_val, max_val, num_args) # Initial parameter values, to be define initial position
    print(f"Current position: {initial_parameter_vals}")
    initial_function_val = func(*initial_parameter_vals) # Function evaluated at the initial parameter values
    current_pos = np.array([*initial_parameter_vals, initial_function_val]) # Current position (coordinates) to be updated with grad descent
    print(f"Initial coordinates are: {current_pos}")

    # for _ in range(max_iterations):

    #   calculate gradient of function
    #   calculate new positions with e.g. X_new, ... = current_pos[0] - learning_rate * X_derivative, ...
    #   update current positions using X_new, ... e.g. current_pos = (X_new, ..., f(X_new, ...))

    for _ in range(max_iterations):

        gradients = calculate_gradient(func, current_pos[:-1])
        



def func(x):
    return x**2

optimised_vals = gradient_descent(func, 1, min_val=0, max_val=1)



