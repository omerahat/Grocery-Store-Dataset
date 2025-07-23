import os
import shutil

# --- SETTINGS ---
# The base directory where the script is located
BASE_DIR = '.' 

# The names of the source folders to be merged
SOURCE_FOLDERS = ['fine_train', 'fine_test', 'fine_val']

# The name of the target folder where the merged dataset will be created
TARGET_FOLDER = 'merged_dataset'


def merge_dataset():
    """
    Merges data from train, test, and val folders into a single target folder,
    preserving the class structure.
    """
    print("Dataset merging process is starting...")
    
    target_path = os.path.join(BASE_DIR, TARGET_FOLDER)
    
    # 1. Create the target folder if it doesn't exist
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        print(f"Target folder created: '{target_path}'")

    total_files_copied = 0

    # 2. Loop through each source folder (train, test, val)
    for source_folder_name in SOURCE_FOLDERS:
        source_path = os.path.join(BASE_DIR, source_folder_name)
        
        if not os.path.isdir(source_path):
            print(f"Warning: '{source_path}' not found, skipping this folder.")
            continue
            
        print(f"\nProcessing '{source_path}'...")
        
        # 3. Find the class folders inside the source folder
        class_folders = [d for d in os.listdir(source_path) if os.path.isdir(os.path.join(source_path, d))]
        
        for class_name in class_folders:
            target_class_path = os.path.join(target_path, class_name)
            
            # 4. Create the class folder in the target directory if it doesn't exist
            if not os.path.exists(target_class_path):
                os.makedirs(target_class_path)

            # 5. Copy all files from the current class folder
            current_class_path = os.path.join(source_path, class_name)
            files = os.listdir(current_class_path)
            
            for file_name in files:
                source_file_path = os.path.join(current_class_path, file_name)
                
                # 6. Create a new filename to prevent naming collisions
                new_file_name = f"{source_folder_name}_{file_name}"
                target_file_path = os.path.join(target_class_path, new_file_name)
                
                # shutil.copy2 preserves file metadata (like creation date, etc.)
                shutil.copy2(source_file_path, target_file_path)
                total_files_copied += 1

    print(f"\nProcess complete! A total of {total_files_copied} files were copied to the '{TARGET_FOLDER}' folder.")


# --- RUN THE SCRIPT ---
if __name__ == "__main__":
    merge_dataset()