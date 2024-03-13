import glob
import os

# Open gradient.txt file 

# Specify spinchain path
spinchain_path = r'/home/hgjones9/spinchain'

# Look for most recent gradient output.txt file
gradient_output = glob.glob(os.path.join(spinchain_path, 'gradient-*'))
print(gradient_output)


