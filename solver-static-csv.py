from z3 import *
import csv

# Function to read data from a CSV file
def read_csv(file_name):
    with open(file_name, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        data = [row for row in reader]
    return data


intersects_data = read_csv('intersects.csv')
Intersects = {(row[0].split(", ")[0], row[0].split(", ")[1]) for row in intersects_data}


has_traffic_data = read_csv('has_traffic.csv')
HasTraffic = {row[0] for row in has_traffic_data}

green_signal_data = read_csv('green_signal.csv')
GreenSignal = {row[0] for row in green_signal_data}

crashes_data = read_csv('crashes.csv')
Crashes = {(row[0].split(", ")[0], row[0].split(", ")[1]) for row in crashes_data}


x, y = String("a"), String("b")

solver = Solver()

#defining constraints
# Adding constraints to the solver
solver.add(intersection_constraint)
solver.add(traffic_constraint)
solver.add(green_signal_constraint)
# Define the crash constraint
crash_constraint = Or([And(x == a, y == b) for a, b in Crashes])

# Add the crash constraint to the solver
solver.add(crash_constraint)

solutions = []
while solver.check() == sat:
    model = solver.model()
    solution = (model[x], model[y])
    reverse_solution = (model[y], model[x])
    
    if solution not in solutions and reverse_solution not in solutions:
        solutions.append(solution)
        print(f"Crash found at: ({solution[0]}, {solution[1]})")
    
    # Add a constraint to avoid the same solution in the next iteration
    solver.add(Or(x != solution[0], y != solution[1]))

if not solutions:
    print("No crashes found.")
