import os
import json

base_directory = "/Users/rdeenik/LocalFiles/GitHub/pure-partner-central/_source"

def rename_directories(base_path):
    for root, dirs, files in os.walk(base_path, topdown=False):  # Bottom-up to avoid renaming parents first
        if "content.json" in files:
            json_path = os.path.join(root, "content.json")
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    if "urlName" in data:
                        new_name = data["urlName"]
                        parent_dir = os.path.dirname(root)
                        new_path = os.path.join(parent_dir, new_name)
                        
                        if os.path.exists(new_path):
                            print(f"Skipping rename: {new_path} already exists.")
                        else:
                            os.rename(root, new_path)
                            print(f"Renamed '{root}' to '{new_path}'")
            except (json.JSONDecodeError, OSError) as e:
                print(f"Error processing {json_path}: {e}")

if __name__ == "__main__":
    if os.path.isdir(base_directory):
        rename_directories(base_directory)
    else:
        print("Invalid directory path.")