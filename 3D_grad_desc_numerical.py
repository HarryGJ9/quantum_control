import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def func1(x, y):
    return np.sin(5 * x) * np.cos(5 * y) / 5

def func2(x, y):
    return x**2 + y**2

def calculate_gradient(x, y, h=1e-6):
    
    df_dx = (func1(x + h, y) - func1(x - h, y)) / (2 * h)
    df_dy = (func1(x, y + h) - func1(x, y - h)) / (2 * h)

    return df_dx, df_dy

def grad_descent(max_iterations=10, learning_rate=0.1, gradient_threshold=1e-3):
    
    # Define x and y values
    x = np.arange(-1, 1, 0.01)
    y = np.arange(-1, 1, 0.01)

    # Form meshgrid of x and y values
    X, Y = np.meshgrid(x, y)
    Z = func1(X, Y)

    # Initialise starting position
    current_pos = np.array([0.1, 0.1, func1(0.1, 0.1)])

    ax = plt.subplot(projection='3d', computed_zorder=False)

    for _ in range(max_iterations):
        
        gradients = calculate_gradient(current_pos[0], current_pos[1])
        print(gradients)
        gradient_norm = np.linalg.norm(gradients)

        if gradient_norm < gradient_threshold:
            break

        X_derivative, Y_derivative = gradients[0], gradients[1]
        X_new, Y_new = current_pos[0] - learning_rate * X_derivative, current_pos[1] - learning_rate * Y_derivative
        current_pos = (X_new, Y_new, func1(X_new, Y_new))
        print(current_pos)

        # ax.plot_surface(X, Y, Z, cmap='viridis', zorder=0)
        # ax.scatter(current_pos[0], current_pos[1], current_pos[2], cmap='magenta', zorder=1)
        # plt.pause(0.001)
        # ax.clear()

    print(f"Calculated minimum = {current_pos[0]:.3f}, {current_pos[1]:.3f}, {current_pos[2]:.3f}")   
    # plt.show()
    


grad_descent()  
