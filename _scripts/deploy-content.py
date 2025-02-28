import os
import json
import shutil

# Define paths
source_directory = "/Users/rdeenik/LocalFiles/GitHub/pure-partner-central/_source"
destination_directories = {
    "uat": "/Users/rdeenik/LocalFiles/GitHub/pure-partner-central/uat",
    "prod": "/Users/rdeenik/LocalFiles/GitHub/pure-partner-central/prod",
    "partnersbx": "/Users/rdeenik/LocalFiles/GitHub/pure-partner-central/partnersbx",
    "fullbackup": "/Users/rdeenik/LocalFiles/GitHub/pure-partner-central/fullbackup",
}

META_FILENAME = "_meta.json"
CONTENT_FILENAME = "content.json"

def load_json(file_path):
    """Load JSON data from a file safely."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Warning: Could not parse JSON in {file_path}")
        return None

def find_matching_dirs(root_dir, target_path):
    """Find directories containing META_FILENAME with matching path value."""
    matching_dirs = []
    for dirpath, _, filenames in os.walk(root_dir):
        if META_FILENAME in filenames:
            meta_data = load_json(os.path.join(dirpath, META_FILENAME))
            if meta_data and meta_data.get("path") == target_path:
                matching_dirs.append(dirpath)
    return matching_dirs

def process_directory(dirpath, filenames):
    """Process a single source directory."""
    if META_FILENAME not in filenames or CONTENT_FILENAME not in filenames:
        return

    meta_data = load_json(os.path.join(dirpath, META_FILENAME))
    if not meta_data or not meta_data.get("path"):
        print(f"Skipping {dirpath} due to missing path in {META_FILENAME}.")
        return
    
    content_file = os.path.join(dirpath, CONTENT_FILENAME)
    source_content = load_json(content_file)
    
    for env, dest_root in destination_directories.items():
        deploy_content(env, dest_root, meta_data["path"], dirpath, content_file, source_content)

def deploy_content(env, dest_root, content_path, source_dir, content_file, source_content):
    """Deploy content to the appropriate environment."""
    matching_dirs = find_matching_dirs(dest_root, content_path)
    
    for matching_dir in matching_dirs:
        dest_content_file = os.path.join(matching_dir, CONTENT_FILENAME)
        dest_content = load_json(dest_content_file)
        
        if dest_content and source_content and dest_content.get("title") == source_content.get("title"):
            print(f"Updating {dest_content_file} in {env}.")
            shutil.copy(content_file, dest_content_file)
            return
    
    # If no exact title match, create new directory structure
    relative_path = os.path.relpath(source_dir, source_directory)
    new_dest_path = os.path.join(dest_root, relative_path)
    os.makedirs(new_dest_path, exist_ok=True)
    dest_content_file = os.path.join(new_dest_path, CONTENT_FILENAME)
    print(f"Creating new content in {dest_content_file} for {env}.")
    shutil.copy(os.path.join(source_dir, META_FILENAME), os.path.join(new_dest_path, META_FILENAME))
    shutil.copy(content_file, dest_content_file)

def deploy_all():
    """Loop through source directories and deploy CONTENT_FILENAME based on META_FILENAME path values."""
    for dirpath, _, filenames in os.walk(source_directory):
        process_directory(dirpath, filenames)

if __name__ == "__main__":
    deploy_all()
