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

meta_file = "_meta.json"
content_file = "content.json"

def load_json(file_path):
    """Load JSON data from a file safely."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Warning: Could not parse JSON in {file_path}")
        return None

def find_matching_dir(root_dir, target_path):
    """Find directory containing _meta.json with matching path value."""
    for dirpath, _, filenames in os.walk(root_dir):
        if meta_file in filenames:
            meta_data = load_json(os.path.join(dirpath, meta_file))
            if meta_data and meta_data.get("path") == target_path:
                return dirpath
    return None

def process_directory(dirpath, filenames):
    """Process a single source directory."""
    if meta_file not in filenames or content_file not in filenames:
        return

    meta_data = load_json(os.path.join(dirpath, meta_file))
    if not meta_data or not meta_data.get("path"):
        print(f"Skipping {dirpath} due to missing path in _meta.json.")
        return
    
    content_file = os.path.join(dirpath, content_file)
    for env, dest_root in destination_directories.items():
        deploy_content(env, dest_root, meta_data["path"], dirpath, content_file)

def deploy_content(env, dest_root, content_path, source_dir, content_file):
    """Deploy content to the appropriate environment."""
    matching_dir = find_matching_dir(dest_root, content_path)
    
    if matching_dir:
        dest_content_file = os.path.join(matching_dir, content_file)
        print(f"Updating {dest_content_file} in {env}.")
    else:
        relative_path = os.path.relpath(source_dir, source_directory)
        new_dest_path = os.path.join(dest_root, relative_path)
        os.makedirs(new_dest_path, exist_ok=True)
        dest_content_file = os.path.join(new_dest_path, content_file)
        print(f"Creating new content in {dest_content_file} for {env}.")
        shutil.copy(os.path.join(source_dir, meta_file), os.path.join(new_dest_path, meta_file))
    
    shutil.copy(content_file, dest_content_file)

def deploy_all():
    """Loop through source directories and deploy content.json based on _meta.json path values."""
    for dirpath, _, filenames in os.walk(source_directory):
        process_directory(dirpath, filenames)

if __name__ == "__main__":
    deploy_all()
