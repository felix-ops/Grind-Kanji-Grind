import csv

input_file = "raw_data/rtk_data_5ed_unstructured.txt"
output_file = "raw_data/rtk_data_5ed_unstructured.csv"

# Define the header and data fields
header = ["heisignumber", "kanji", "keyword3rd-ed", "keyword4th-ed", "keyword5th-ed", "strokecount", "indexordinal", "lessonnumber"]
data = []

# Read the input file
with open(input_file, "r", encoding="utf-8") as file:
    # Skip comment lines
    for line in file:
        if line.startswith("#"):
            continue
        
        # Split each line by colon (:)
        fields = line.strip().split(":")
        
        # Append data as dictionary
        data.append({header[i]: fields[i] for i in range(len(header))})

# Sort the data by heisignumber
sorted_data = sorted(data, key=lambda x: int(x['heisignumber']))

# Write the sorted data to CSV
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    
    # Write the header
    writer.writeheader()
    
    # Write the data
    for entry in sorted_data:
        writer.writerow(entry)

print("CSV file has been created successfully.")
