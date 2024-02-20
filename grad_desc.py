

# Define loss function to be minimised

# Define function that calculates the gradient of the loss function 

import numpy as np

def derivative(f, a, h=1e-6):
   return (f(a + h) - f(a - h)) / (2 * h)

def numerical_gradient(func, *args, h=1e-3):

    # for each parameter in the function, take its derivative using the central difference method and append it to a list containing the gradients
    gradient = []
    for arg in args:
       print(arg)
       gradient.append(derivative(func,arg))
       print(gradient)
    return gradient



# Define function to calculate gradient descent 