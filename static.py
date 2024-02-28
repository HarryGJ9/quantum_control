
# IN UBUNTU, RUN FROM SPINCHAIN DIRECTORY
file_path = r'/output-latest/data/dynamics_formatted.data'

with open(file_path, 'r') as file:
    content=file.read()
    print(content)