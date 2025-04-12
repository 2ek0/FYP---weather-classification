import os
import shutil

# Define source and destination folders
source_dir = r"D:\2025"
destination_dir = r"D:\Image"

# Ensure the destination folder exists
os.makedirs(destination_dir, exist_ok=True)

# Walk through all subdirectories and copy files
for root, _, files in os.walk(source_dir):
    for file in files:
        source_path = os.path.join(root, file)
        destination_path = os.path.join(destination_dir, file)

        # Ensure unique filenames if duplicates exist
        counter = 1
        while os.path.exists(destination_path):
            file_name, file_ext = os.path.splitext(file)
            destination_path = os.path.join(destination_dir, f"{file_name}_{counter}{file_ext}")
            counter += 1

        # Copy file
        shutil.copy2(source_path, destination_path)

print("✅ All files copied successfully to", destination_dir)
