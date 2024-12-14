from z3 import *
import csv 

def read_csv(file_name):
    with open(file_name, mode='r+', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        data = [row for row in reader]
    return data

def write_csv(file_name, data, header=None):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(header)
        writer.writerows(data)

intersects_data = read_csv('intersects.csv')
Intersects = {(row[0], row[1]) for row in intersects_data}


has_traffic_data = read_csv('has_traffic.csv')
HasTraffic = {row[0] for row in has_traffic_data}

green_signal_data = read_csv('green_signal.csv')
GreenSignal = {row[0] for row in green_signal_data}

crashes_data = read_csv('crashes.csv')
Crashes = {(row[0].split(", ")[0], row[0].split(", ")[1]) for row in crashes_data}

solver = Solver()

traffic = {street: Bool(f"traffic_{street}") for street in HasTraffic | GreenSignal}
signal = {street: Bool(f"signal_{street}") for street in HasTraffic | GreenSignal}

for street in traffic:
    solver.add(traffic[street] == (street in HasTraffic))
    solver.add(signal[street] == (street in GreenSignal))

crash_vars = {}
for (street1, street2) in Intersects:
    crash_var = Bool(f"crash_{street1}_{street2}")
    crash_vars[(street1, street2)] = crash_var
    solver.add(crash_var == And(traffic[street1], signal[street1], traffic[street2], signal[street2]))

for (street1, street2) in Crashes:
    solver.add(crash_vars[(street1, street2)] == True)

potential_crashes = []
if solver.check() == sat:
    model = solver.model()
    for (street1, street2), crash_var in crash_vars.items():
        if model[crash_var]:
            conditions = []
            if model[traffic[street1]]:
                conditions.append(f"traffic_{street1}")
            if model[signal[street1]]:
                conditions.append(f"signal_{street1}")
            if model[traffic[street2]]:
                conditions.append(f"traffic_{street2}")
            if model[signal[street2]]:
                conditions.append(f"signal_{street2}")
            potential_crashes.append((street1, street2))
            print(f"Crash at ({street1}, {street2}) occurs if:")
            print(f"  {' AND '.join(conditions)}")
else:
    print("No solution found.")

print("\nAdditional crashes detected:")
for crash in potential_crashes:
    if crash not in Crashes:
        print(f"  Crash at {crash}")

    new_crashes = [crash for crash in potential_crashes]
    if new_crashes:
        write_csv('answer.csv', new_crashes, ["Street1", "Street2"])
