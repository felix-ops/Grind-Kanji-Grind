import csv

input_file = "raw_data/rtk_data_6ed.csv"
output_file = "raw_data/RTK_6ED.csv"

column1_key = "kanji"
column2_key = "keyword_6th_ed"
# Read the CSV file and filter data
filtered_data = []
with open(input_file, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Check if both kanji and keyword5th-ed columns exist in the row
        if column1_key in row and column2_key in row:
            # Append kanji and keyword5th-ed values to filtered_data
            filtered_data.append([row[column1_key], row[column2_key]])

# Write the filtered data to a new CSV file
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    
    # Write filtered data
    writer.writerows(filtered_data)

print("Filtered CSV file has been created successfully.")
