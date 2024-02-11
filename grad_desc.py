import numpy as np

def fitness(Fmax, tf, Jmax, a=1, b=0.01):

    return 100 * np.exp(a(Fmax - 1)) * np.exp(b * tf * Jmax)

def grad(J, h):

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