import os
import re

# Define the directory containing the files
directory = "/Users/rdeenik/LocalFiles/GitHub/pure-partner-central/_source/P1 Learn/P13 Products/P133 Archive and Backup"  # Change this to your target directory

# Define search and replace values as variables
search_replace_pairs = {
    "P131": "P133",
    "C131": "C133",
    "I131": "I133",
    "i131": "i133",
    "UBF": "AAB",
    "ubf": "aab",
    "Unified Block and File": "Archive and Backup"
}

# Function to recursively process JSON files in the directory
def search_and_replace_json(directory, search_replace_pairs):
    for root, dirs, files in os.walk(directory, topdown=False):  # Use `topdown=False` to rename subdirectories first
        # Process files
        for filename in files:
            if filename.endswith(".json"):  # Only process JSON files
                file_path = os.path.join(root, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()

                    # Perform search and replace inside file content
                    for search, replace in search_replace_pairs.items():
                        content = re.sub(re.escape(search), replace, content)

                    # Write changes back to the file
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)

                    print(f"Updated content in: {file_path}")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        # Rename directories
        for dir_name in dirs:
            new_dir_name = dir_name
            for search, replace in search_replace_pairs.items():
                new_dir_name = re.sub(re.escape(search), replace, new_dir_name)
            
            if new_dir_name != dir_name:  # Only rename if changes are made
                old_dir_path = os.path.join(root, dir_name)
                new_dir_path = os.path.join(root, new_dir_name)
                try:
                    os.rename(old_dir_path, new_dir_path)
                    print(f"Renamed directory: {old_dir_path} → {new_dir_path}")
                except Exception as e:
                    print(f"Error renaming directory {old_dir_path}: {e}")

        # Rename files
        for filename in files:
            new_filename = filename
            for search, replace in search_replace_pairs.items():
                new_filename = re.sub(re.escape(search), replace, new_filename)

            if new_filename != filename:  # Only rename if changes are made
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, new_filename)
                try:
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed file: {old_file_path} → {new_file_path}")
                except Exception as e:
                    print(f"Error renaming file {old_file_path}: {e}")

# Run the function
search_and_replace_json(directory, search_replace_pairs)