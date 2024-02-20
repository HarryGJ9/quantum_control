import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def z_func(x, y):
    return np.sin(5 * x) * np.cos(5 * y) / 5

def calculate_gradient(x, y):
    return np.cos(5 * x) * np.cos(5 * y), - np.sin(5 * x) * np.sin(5 * y)

x = np.arange(-1,1,0.01)
y = np.arange(-1,1,0.01)

X, Y = np.meshgrid(x, y)
Z = z_func(X, Y)

current_pos1 = (0.7, 0.4, z_func(0.7, 0.4))
current_pos2 = (0.3, 0.8, z_func(0.3, 0.8))
current_pos3 = (-0.5, 0.3, z_func(0.1, 0.5))
learning_rate = 0.01
max_iterations = 1000

ax = plt.subplot(projection='3d', computed_zorder=False)

for _ in range(max_iterations):

    X_derivative, Y_derivative = calculate_gradient(current_pos1[0], current_pos1[1])
    X_new, Y_new  = current_pos1[0] - learning_rate * X_derivative, current_pos1[1] - learning_rate * Y_derivative
    current_pos1 = (X_new, Y_new, z_func(X_new, Y_new))

    X_derivative, Y_derivative = calculate_gradient(current_pos2[0], current_pos2[1])
    X_new, Y_new  = current_pos2[0] - learning_rate * X_derivative, current_pos2[1] - learning_rate * Y_derivative
    current_pos2 = (X_new, Y_new, z_func(X_new, Y_new))
    
    X_derivative, Y_derivative = calculate_gradient(current_pos3[0], current_pos3[1])
    X_new, Y_new  = current_pos3[0] - learning_rate * X_derivative, current_pos3[1] - learning_rate * Y_derivative
    current_pos3 = (X_new, Y_new, z_func(X_new, Y_new))

    
    ax.plot_surface(X, Y , Z, cmap='viridis', zorder=0)
    ax.scatter(current_pos1[0], current_pos1[1], current_pos1[2], cmap="magenta", zorder=1)
    ax.scatter(current_pos2[0], current_pos2[1], current_pos2[2], cmap="red", zorder=1)
    ax.scatter(current_pos3[0], current_pos3[1], current_pos3[2], cmap="blue", zorder=1)
    plt.pause(0.001)
    ax.clear()

plt.show()

    
    




