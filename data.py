import csv

# Define the data with 20 entries, including duplicates
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "Los Angeles"],
    ["Charlie", 35, "Chicago"],
    ["Diana", 28, "Miami"],
    ["Eve", 22, "Boston"],
    ["Alice", 30, "New York"],
    ["Frank", 40, "Houston"],
    ["Grace", 27, "Seattle"],
    ["Hank", 32, "San Francisco"],
    ["Ivy", 24, "Denver"],
    ["Bob", 25, "Los Angeles"],
    ["Charlie", 35, "Chicago"],
    ["Jack", 29, "Austin"],
    ["Kim", 31, "Dallas"],
    ["Leo", 33, "Orlando"],
    ["Mia", 26, "Las Vegas"],
    ["Nina", 23, "Portland"],
    ["Oscar", 34, "Phoenix"],
    ["Alice", 30, "New York"],
    ["Paul", 28, "Philadelphia"],
    
]

# Write the data to a CSV file
with open('duplicate_data_20_entries.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV file with 20 entries including duplicates created successfully.")
