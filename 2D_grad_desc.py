import matplotlib.pyplot as plt
import numpy as np

# Define loss function (difference between the desired value and measured value)
# Take gradient of loss function
# Pick random values for parameters
# Plug parameters values into the gradient 
# Calculate step sizes: step_size = slop * learning rate
# Calculate new parameters: new_parameter = old_parameter - step_size
# Repeat until converge on a step_size ~ 0



def func(x):
    return x ** 3

def func_gradient(x):
    return 3 * x

x  = np.arange(-100,100,0.01)
y = func(x)

current_pos = (80, func(80))
learning_rate = 0.01

for _ in range(1000):
    new_x = current_pos[0] - learning_rate * func_gradient(current_pos[0])
    new_y = func(new_x)
    current_pos = (new_x, new_y)

    plt.plot(x, y)
    plt.scatter(current_pos[0], current_pos[1], color="red")
    plt.pause(0.001)
    plt.clf()



