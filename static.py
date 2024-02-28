
# Specify path to dynamics_formatted.data
dynamics_path = r'/home/hgjones9/spinchain/output-latest/data/dynamics_formatted.data'

# Create empty dictionary in which to add fidelity at a specified time
data = {}

# Open and read file
with open(dynamics_path, 'r') as file:

    next(file) # Skip the first line as this is the title

    # For each row of data, strip edge whitespace and separate by one whitespace
    for row in file:
        values = row.strip.split()

        # If there are values in the row (i.e. not blank space):
        # Return the time, rounded to 2 d.p.
        # Append the dictionary to include the fidelity value at a specific time
        if values:
            time = round(float(values[0]), 2)
            data[time] = values[1]


# Specify time at which to calculate fidelity
target_time = input("Input time (to 2 d.p. to calculate fidelity: ")

# Check that the time given is in the given data range
if target_time > 20 or target_time < 0:
    raise Exception("Time must be between 0 and 20")

# Return fidelity at the target time
fidelity = data[target_time]
print(f"Fidelity wrt to target state at t={target_time} is {fidelity}")













