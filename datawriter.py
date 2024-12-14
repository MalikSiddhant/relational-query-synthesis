import csv

Intersects = {
    ("Broadway", "Liberty St"),
    ("Broadway", "Wall St"),
    ("Broadway", "Whitehall"),
    ("Liberty St", "Broadway"),
    ("Liberty St", "William St"),
    ("Wall St", "Broadway"),
    ("Wall St", "William St"),
    ("Whitehall", "Broadway"),
    ("William St", "Liberty St"),
    ("William St", "Wall St"),
}

# Adjusted to ensure overlapping conditions for multiple intersections
HasTraffic = {"Broadway", "Wall St", "William St", "Whitehall", "Liberty St"}
GreenSignal = {"Broadway", "Liberty St", "William St", "Whitehall", "Wall St"}
Crashes = {("Whitehall", "Broadway")}

# Write Intersects data to CSV
with open('intersects.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Street1", "Street2"])
    for intersection in Intersects:
        writer.writerow(intersection)

# Write HasTraffic data to CSV
with open('has_traffic.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["HasTraffic"])
    for street in HasTraffic:
        writer.writerow([street])

# Write GreenSignal data to CSV
with open('green_signal.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["GreenSignal"])
    for street in GreenSignal:
        writer.writerow([street])

# Write Crashes data to CSV
with open('crashes.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Crashes"])
    for crash in Crashes:
        writer.writerow([f"{crash[0]}, {crash[1]}"])

print("CSV files created successfully.")