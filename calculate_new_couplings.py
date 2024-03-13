import glob
import os
import numpy as np

########################
# OPEN GRADIENT.TXT FILE
########################

# # Specify spinchain path
# spinchain_path = r'/home/hgjones9/spinchain'

# Test spinchain path
spinchain_path = 'C:\\Users\harry\quantum_control\outputs_practice'

# Look for most recent gradient output.txt file
gradient_output = glob.glob(os.path.join(spinchain_path, 'gradient-*'))
print(gradient_output)

# BELOW NOT WORKING DUE TO ABOVE BEING A LIST

# if os.path.exists(gradient_output):

#     # Read gradient.txt file
#     with open(gradient_output, 'r') as file:
#         gradient = np.loadtxt(data, dtype=float)
#         print(gradient)
# else: 
#     print("No gradient.txt file found.")






