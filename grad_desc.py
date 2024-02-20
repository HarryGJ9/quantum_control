import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

#########################################################
# PRACTICE GRADIENT DESCENT ALG, PERFORMED ON A MULTIVARIABLE ANALYTIC FUNCTION
#########################################################

# Define loss function
# Here we use f(x,y) = x^2 + y^2
def func(x, y):
    return x**2 + y**2

# Plot function if we want
def plot(func):   
    x = np.linspace(-100,100,100)
    y = np.linspace(-100,100,100)

    # Plot function
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)

    ax.plot_wireframe(X,Y,Z, rstride=10, cstride=10)
    plt.show()

# Calculate the gradient of the loss function
def gradient_calculator(f, h=0.01):


    # for each parameter in the function
    # calculate the derivative of the function wrt to that parameter (partial derivative)
    # add that derivative to a the gradient vector

    gradient = []
    for i in params:
        derivative = (f(i + h) - f(i - h)) / (2 * h)
        gradient.append(derivative)
    
    print(gradient)


# Define loss function: here it is our fitness that we want to optimise
def fitness(Fmax, tf, Jmax, a=1, b=0.01):

    return 100 * np.exp(a(Fmax - 1)) * np.exp(b * tf * Jmax)



# Take the gradient of the fitness (loss) function with respect to the couplings
# For now I will assume an analytic function of two variables: F(x,y)



def coupling_gradient(J, h):

    return ((J + h) - (J - h)) / (2 * h)

def grad_fitness(Fmax, tf, Jmax, h=10):

    # for a given fitness function evaluation, return the gradient of it wrt the coupling value

    # Define couplings
    J1 = 550
    J2 = 500

    f = fitness(Fmax, tf, Jmax)

    couplings = [J1, J2]

    grad_f = grad(J1, h)

    return grad_f