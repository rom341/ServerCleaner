import os
import json
import time
from datetime import datetime, timezone

# Configuration
DOWNLOADED_DIRECTORIES_FILENAME = "/etc/auto_remover/downloaded_directories.txt" # file that contains the list of downloaded directories
CHECK_INTERVAL_SECONDS = 30  # how often program should check downloaded directories
DELETE_DIRECTORY_TIME_CAP_SECONDS = CHECK_INTERVAL_SECONDS * 2 # how much time must pass before the file can be deleted

def read_downloaded_directories_file():
    if not os.path.exists(DOWNLOADED_DIRECTORIES_FILENAME):
        with open(DOWNLOADED_DIRECTORIES_FILENAME, 'w') as f:
            pass  # Simply create an empty file
        return []
    with open(DOWNLOADED_DIRECTORIES_FILENAME, 'r') as f:
        directories = [line.strip() for line in f if line.strip()]
    return directories

def write_directory_list_to_file(directories):
    """Overwrite the file with the updated list of directories."""
    with open(DOWNLOADED_DIRECTORIES_FILENAME, 'w') as f:
        for directory in directories:
            f.write(f"{directory}\n")

def remove_directory(directory):
    try:
        # Remove the directory and all its contents
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(directory)
        print(f"Directory {directory} successfully removed.")
    except Exception as e:
        print(f"Error removing directory {directory}: {e}")
    directories = read_downloaded_directories_file()
    updated_directories = [d for d in directories if d != directory]
    write_directory_list_to_file(updated_directories)

def clear_directories():
    directories = read_downloaded_directories_file()
    current_time = datetime.now(timezone.utc)
    for directory in directories:
        auto_remove_path = os.path.join(directory, "auto_remove.json")
        if not os.path.exists(auto_remove_path):
            print(f"File {auto_remove_path} not found. Skipping directory.")
            continue
        try:
            with open(auto_remove_path, 'r') as f:
                data = json.load(f)
            last_sync_time = datetime.strptime(data["last_sync_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
            time_diff = (current_time - last_sync_time).total_seconds()
            if time_diff > DELETE_DIRECTORY_TIME_CAP_SECONDS:
                remove_directory(directory)
        except Exception as e:
            print(f"Error processing {auto_remove_path}: {e}")

def main():
    while True:
        print(f"Starting directory check at {datetime.now(timezone.utc)}Z")
        clear_directories()
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
