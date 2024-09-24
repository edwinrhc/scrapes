import pandas as pd

# Step 1: Load the CSV files into DataFrames
csv1 = pd.read_csv('ecoquality_products_v4.csv', keep_default_na=False, low_memory=False)
csv2 = pd.read_csv('ecoquality_products_v5.csv', keep_default_na=False, low_memory=False)
csv3 = pd.read_csv('ecoquality_products_v6.csv', keep_default_na=False, low_memory=False)
csv4 = pd.read_csv('ecoquality_products_v3.csv', keep_default_na=False, low_memory=False)

# Step 2: Calculate the number of rows in each DataFrame to determine the missing rows
# (This step is actually optional if you're simply appending all extra rows from csv1 to csv2)

# Step 3: Append the missing rows from csv1 to csv2
# Since the first Y rows are the same, and assuming the order is the same,
# we can simply append the rows from csv1 starting from Y (the length of csv2) to the end
missing_rows = csv4[len(csv3):]
updated_csv2 = pd.concat([csv3, missing_rows], ignore_index=True)

# # Step 4: Save the updated DataFrame to a new CSV file
updated_csv2.to_csv('ecoquality_products_v7.csv', index=False)

print(f"Length of csv1: {len(csv1)}")
print(f"Length of csv2: {len(csv2)}")
print(f"Length of csv3: {len(csv3)}")
print(f"Length of csv4: {len(csv4)}")
print(f"Length of updated_csv2: {len(updated_csv2)}")

# Print first 5 rows titles and last 5 rows titles from all csv


# print("First 5 rows titles from csv1:")
# for i in range(5):
#     print(f"First 5 rows: {csv1['title'][i]}")

# print("First 5 rows titles from csv2:")

# for i in range(5):
#     print(f"First 5 rows: {csv2['title'][i]}")

# print("First 5 rows titles from csv3:")
# for i in range(5):
#     print(f"First 5 rows: {csv3['title'][i]}")

# print("First 5 rows titles from csv4:")
# for i in range(5):
#     print(f"First 5 rows: {csv4['title'][i]}")

# print("Last 5 rows titles from csv1:")
# for i in range(len(csv1)-5, len(csv1)):
#     print(f"Last 5 rows: {csv1['title'][i]}")

# print("Last 5 rows titles from csv2:")
# for i in range(len(csv2)-5, len(csv2)):
#     print(f"Last 5 rows: {csv2['title'][i]}")

# print("Last 5 rows titles from csv3:")
# for i in range(len(csv3)-5, len(csv3)):
#     print(f"Last 5 rows: {csv3['title'][i]}")

# print("Last 5 rows titles from csv4:")
# for i in range(len(csv4)-5, len(csv4)):
#     print(f"Last 5 rows: {csv4['title'][i]}")

# # Print the last 5 rows of csv4 from index len(csv1)
# print("Last 5 rows titles from csv4 from index len(csv1):")
# for i in range(len(csv1) - 5, len(csv1)):
#     print(f"Last 5 rows: {csv4['title'][i]}")
