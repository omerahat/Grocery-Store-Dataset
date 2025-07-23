import os
import csv
from collections import Counter

# List of the main directories to scan
directories_to_scan = ['merged_dataset']

# A Counter object is used to easily find and store unique product names.
grand_total_counts = Counter()

# Main loop to iterate through all specified directories
for directory in directories_to_scan:
    print(f"\n--- Scanning Directory: '{directory}' ---")
    
    if not os.path.isdir(directory):
        print(f"WARNING: Directory '{directory}' not found. Skipping.")
        continue

    # Find the products (subdirectories) in the directory
    for product_folder in os.listdir(directory):
        path = os.path.join(directory, product_folder)
        
        # If it's a directory, consider it a product
        if os.path.isdir(path):
            # We use the Counter to ensure each product name is added to our list just once.
            grand_total_counts[product_folder] += 1
            
    if grand_total_counts:
        print(f"Found {len(grand_total_counts)} unique product folders in '{directory}'.")
    else:
        print("No product folders were found in this directory.")

# --- Report and CSV Export ---
print("\n" + "="*45)
print("       EXPORTING PRODUCT LIST TO CSV")
print("="*45)

if not grand_total_counts:
    print("\nNo data was found to export.")
else:
    # Get only the product names (the keys of the Counter) and sort them alphabetically
    product_names = sorted(grand_total_counts.keys())
    
    print(f"\nTotal Unique Products: {len(product_names)}")

    # --- Export to CSV File ---
    csv_file_name = 'product_list_report.csv'
    print(f"\nExporting product list to '{csv_file_name}'...")

    try:
        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            # Define the header
            header = ['Product']
            csv_writer = csv.writer(csvfile)
            
            # Write the header row
            csv_writer.writerow(header)
            
            # Write the data rows (only the product names)
            for product in product_names:
                csv_writer.writerow([product])

        print(f"✅ Successfully exported the report.")

    except IOError:
        print(f"❌ ERROR: Could not write to the file {csv_file_name}.")