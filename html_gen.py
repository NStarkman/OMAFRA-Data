#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Creates an html document filled with the specifications for a table displaying
# the pest data for each county in the list to be put in the weekly postings.
#Created by Mariaelisa Polsinelli for OMAFRA, 2022 and Nathan Starkman for OMAFRA, 2023
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import csv
import datetime
import matplotlib.pyplot as plt


file_path = 'C:\\Users\\StarkmNa\\Documents\\Code\\OMAFRA-main\\vcr_dashboard_data.csv'

# Getting the current year
current_year = datetime.datetime.now().year

# Ordered counties with stars included
ordered_counties = ["Bruce***", "Essex*", "Chatham-Kent*", "Norfolk**", "Huron***", "Wellington Centre**", "Wellington North**", "Simcoe***", "Durham***", "Peterborough", "Kemptville***", "Sudbury***", "Timiskaming***", "Lambton**", "Thunder Bay", "Middlesex**", "Renfrew"]

pests = {
    "Carrot Rust Fly": 8,
    "Onion Maggot": 9,
    "Carrot Weevil": 10,
    "Aster Leafhopper": 11,
    "Tarnished Plant Bug": 12,
    "Cabbage Maggot": 13,
    "Seedcorn Maggot": 14,
    "European Corn Borer": 15
}

# Strip the stars from the county names for indexing purposes in the results dictionary
counties = [county.rstrip('*') for county in ordered_counties]
results = {county: {pest: 0 for pest in pests} for county in counties}

with open(file_path, mode='r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header

    for index, row in enumerate(reader, 1):
        try:
            row_year = int(row[3].split('-')[0])
        except:
            print(f"Error parsing date in row {index}.")
            continue

        if len(row) > max(pests.values()) and row[2] in counties and row_year == current_year:
            for pest, col_num in pests.items():
                try:
                    value = float(row[col_num])
                    results[row[2]][pest] += value
                except ValueError:
                    print(f"Error converting value '{row[col_num]}' in row {index}, column {col_num + 1}.")

# Printing the results in a formatted manner
column_width = 20
print("Pest".ljust(column_width), end='')
for pest_name in pests.keys():
    print(f"{pest_name}".center(column_width), end='')
print()

print("THRESHOLD".ljust(column_width), end='')
print("329-395, 1399-1711".center(column_width), end='')
print("210-700, 1025-1515".center(column_width), end='')
print("138-156, 455+".center(column_width), end='')
print("128+".center(column_width), end='')
print("40+".center(column_width), end='')
print("314-398, 847-960, 1446-1604".center(column_width), end='')
print("200-350, 600-750, 1000-1150".center(column_width), end='')
print("See legend below".center(column_width))
print('-' * (column_width * (len(pests) + 1)))

# Using ordered_counties to print results in the desired order
for county_name in ordered_counties:
    stripped_name = county_name.rstrip('*')
    print(f"{county_name}".ljust(column_width), end='')
    for pest_value in results[stripped_name].values():
        print(f"{int(pest_value)}".center(column_width), end='')
    print()

class Pest:
    def __init__(self, name, threshold_ranges):
        self.name = name
        self.threshold_ranges = threshold_ranges

def check_thresh(num, pos):
    at_threshold = False
    for t in pest_list[pos].threshold_ranges:
        if isinstance(t, int):
            if num >= t:
                at_threshold = True
        elif isinstance(t, tuple):
            if t[0] <= num <= t[1]:
                at_threshold = True
    return at_threshold

pest_list = [
    Pest("Carrot Rust Fly", [(329, 395), (1399, 1711)]),
    Pest("Onion Maggot", [(210, 700), (1025, 1515)]),
    Pest("Carrot Weevil", [(138, 156), 455]),
    Pest("Aster Leafhopper", [128]),
    Pest("Tarnished Plant Bug", [40]),
    Pest("Cabbage Maggot", [(314, 398), (847, 960), (1446, 1604)]),
    Pest("Seedcorn Maggot", [(200, 350), (600, 750), (1000, 1150)]),
    Pest("European Corn Borer", [1000000])
]

table_start = "<figure class=\"wp-block-table\"><table><tbody><tr><td>County</td>"
threshold_row = "<tr><td>THRESHOLD</td><td>329-395, 1399-1711</td><td>210-700, 1025-1515</td>" \
                "<td>138-156, 455+</td><td>128+</td><td>40+</td><td>314-398, 847-960, 1446-1604</td>" \
                "<td>200-350, 600-750, 1000-1150</td><td>See legend below</td></tr>"
table_end =  "</tbody></table></figure>"
row_start = "<tr>"
row_end = "</tr>"
cell_start = "<td>"
cell_end = "</td>"
threshold = "<span style=\"color:red; font-weight:bold;\">"
end_thresh = "</strong></span>"

wp_table = table_start

for pest in pest_list:
    wp_table = wp_table + cell_start + pest.name + cell_end

wp_table = wp_table + row_end + threshold_row

# Populate the table using the results dictionary
for county_name in ordered_counties:
    wp_table = wp_table + row_start + cell_start + county_name + cell_end
    for i, pest_value in enumerate(results[county_name.rstrip('*')].values()):
        tstat = check_thresh(pest_value, i)
        if tstat:
            wp_table = wp_table + cell_start + threshold + str(int(pest_value)) + end_thresh + cell_end
        else:
            wp_table = wp_table + cell_start + str(int(pest_value)) + cell_end
    wp_table = wp_table + row_end

wp_table = wp_table + table_end
print(wp_table)

html_file_path = "C:/Users/StarkmNa/Documents/Code/OMAFRA-main/pest_table.html"
with open(html_file_path, "w") as html_file:
    html_file.write(wp_table)