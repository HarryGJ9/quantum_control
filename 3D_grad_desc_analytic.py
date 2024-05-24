# ####################################################
# # Performs gradient descent on a 3D analytic function 
# ####################################################


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Function to be minimised (loss function). Chosen arbitrarily.
def z_func(x, y):
    return  np.sin(5 * x) * np.cos(5 * y) / 5

# Function to calculate gradient of the loss function 
def calculate_gradient(x, y):
    return np.cos(5 * x) * np.cos(5 * y), - np.sin(5 * x) * np.sin(5 * y)

# Initialise x & y values
x = np.arange(-1,1,0.01)
y = np.arange(-1,1,0.01)

# Form a grid and calculate landscape height
X, Y = np.meshgrid(x, y)
Z = z_func(X, Y)

# initialise current positions
current_pos1 = (0.25, -0.6, z_func(0.25, -0.6))
# current_pos2 = (0.3, 0.8, z_func(0.3, 0.8))
# current_pos3 = (-0.5, 0.3, z_func(0.1, 0.5))

# specify learning rate and maximum number of iterations
learning_rate = 0.05
max_iterations = 1000

# initialise figure
ax = plt.subplot(projection='3d', computed_zorder=False)

# for each iteration, calculate the gradient at the current position and specify new positions
# plot the current position at each iteration and animate its change
for _ in range(max_iterations):

    X_derivative, Y_derivative = calculate_gradient(current_pos1[0], current_pos1[1])
    X_new, Y_new  = current_pos1[0] + learning_rate * X_derivative, current_pos1[1] + learning_rate * Y_derivative
    current_pos1 = (X_new, Y_new, z_func(X_new, Y_new))

    # X_derivative, Y_derivative = calculate_gradient(current_pos2[0], current_pos2[1])
    # X_new, Y_new  = current_pos2[0] + learning_rate * X_derivative, current_pos2[1] - learning_rate * Y_derivative
    # current_pos2 = (X_new, Y_new, z_func(X_new, Y_new))
    
    # X_derivative, Y_derivative = calculate_gradient(current_pos3[0], current_pos3[1])
    # X_new, Y_new  = current_pos3[0] + learning_rate * X_derivative, current_pos3[1] - learning_rate * Y_derivative
    # current_pos3 = (X_new, Y_new, z_func(X_new, Y_new))

    
    ax.plot_surface(X, Y , Z, cmap='viridis', zorder=0)
    ax.scatter(current_pos1[0], current_pos1[1], current_pos1[2], c="red", cmap="magenta", zorder=1)
    # ax.scatter(current_pos2[0], current_pos2[1], current_pos2[2], cmap="red", zorder=1)
    # ax.scatter(current_pos3[0], current_pos3[1], current_pos3[2], cmap="black", zorder=1)
    plt.pause(1)
    ax.clear()

plt.show()





    
    




