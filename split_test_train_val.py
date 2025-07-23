import os
import shutil
import pandas as pd
import random
import math

# --- Settings ---

CSV_FILE_PATH = 'product_counts_report.csv'
SOURCE_IMAGE_FOLDER = 'merged_dataset'
DESTINATION_FOLDER = 'dataset'
MINIMUM_IMAGE_COUNT = 50

# --- Main Script ---

def create_and_split_class_files(product_name):
    """
    Finds all images for a product, splits them into train/val/test,
    and copies them to the correct destination folders.
    """
    source_product_path = os.path.join(SOURCE_IMAGE_FOLDER, product_name)
    
    # Check if the product source folder exists
    if not os.path.isdir(source_product_path):
        print(f"  - WARNING: Source directory not found for '{product_name}'. Skipping.")
        return

    # Get a list of all image files in the source directory
    try:
        # Filter for files, ignore subdirectories if any
        files = [f for f in os.listdir(source_product_path) if os.path.isfile(os.path.join(source_product_path, f))]
    except OSError as e:
        print(f"  - ERROR: Could not read files for '{product_name}'. Reason: {e}. Skipping.")
        return
        
    if not files:
        print(f"  - INFO: No files found in '{source_product_path}'. Skipping.")
        return

    # Shuffle the list of files randomly
    random.shuffle(files)
    
    # Define split ratios
    train_ratio = 0.7
    val_ratio = 0.15
    
    # Calculate the number of files for each set
    train_count = math.ceil(len(files) * train_ratio)
    val_count = math.ceil(len(files) * val_ratio)
    
    # Split the file list
    train_files = files[:train_count]
    val_files = files[train_count : train_count + val_count]
    test_files = files[train_count + val_count :]

    # Data structure to hold file lists and their destination
    splits = {
        'train': train_files,
        'validation': val_files,
        'test': test_files
    }

    # Copy files to their new destination
    for split_name, file_list in splits.items():
        if not file_list:
            continue
            
        # Create destination folder (e.g., train_dataset/train/Satsumas)
        destination_path = os.path.join(DESTINATION_FOLDER, split_name, product_name)
        os.makedirs(destination_path, exist_ok=True)
        
        for file_name in file_list:
            source_file_path = os.path.join(source_product_path, file_name)
            destination_file_path = os.path.join(destination_path, file_name)
            shutil.copy2(source_file_path, destination_file_path) # copy2 preserves metadata
            
    print(f"  - Split '{product_name}': {len(train_files)} train, {len(val_files)} val, {len(test_files)} test.")


def main():
    """
    Main function to run the data preparation process.
    """
    print("Starting the dataset preparation script...")
    print("This script will split files *within* each class folder.")

    # 1. Read and filter the CSV file
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        df_filtered = df[df['Total_Count'] > MINIMUM_IMAGE_COUNT].copy()
        print(f"\nFound {len(df_filtered)} product classes with more than {MINIMUM_IMAGE_COUNT} images.")
    except FileNotFoundError:
        print(f"ERROR: The file '{CSV_FILE_PATH}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    if df_filtered.empty:
        print("No products met the minimum image count. Exiting.")
        return

    # 2. Iterate through each product class and process its files
    print("\nProcessing each product class:")
    for index, row in df_filtered.iterrows():
        product_name = row['Product']
        create_and_split_class_files(product_name)

    print("\nDataset preparation script finished successfully!")


if __name__ == '__main__':
    main()