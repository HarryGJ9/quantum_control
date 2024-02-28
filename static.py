import os

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the relative path to the data file
file_path = os.path.join(current_directory, '../../spinchain/output-latest/data/dynamics_formatted.data')

try:
    with open(file_path, 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print("An error occurred:", e)

    