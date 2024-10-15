import os
import json
import time
import ftplib
import schedule
from datetime import datetime, timezone, timedelta, UTC

DIRECTORIES_TRANSFER_PLAN = "ftp/directories_transfer_plan.json"  # File with the plan specifying which client directory must be moved to which server directory
REMOTE_DOWNLOADED_DIRECTORIES_FILE = "/etc/auto_remover/downloaded_directories.txt"  # File on the server that contains the list of downloaded directories
AUTO_REMOVE_FILES_SYNC_TIMER_SECONDS = 30  # How often the program needs to sync auto_remove files with the server
AUTO_REMOVE_FILES_SYNC_TIME_STEP_SECONDS = 60  # How much time the program adds to auto_remove files during sync

# FTP settings
FTP_HOST = "192.168.205.137"
FTP_PORT = 21
FTP_USERNAME = "ftpuser"
FTP_PASSWORD = "ftpuser"

def create_auto_remove_file(path):
    current_time = datetime.now(UTC)
    auto_remove = {
        "creation_time": current_time.isoformat(),
        "last_sync_time": (current_time + timedelta(seconds=AUTO_REMOVE_FILES_SYNC_TIME_STEP_SECONDS)).isoformat()
    }
    auto_remove_path = os.path.join(path, "auto_remove.json")
    with open(auto_remove_path, 'w') as f:
        json.dump(auto_remove, f, indent=4)
    print(f"Created file: auto_remove.json in {path}")

def load_transfer_plan():
    if not os.path.exists(DIRECTORIES_TRANSFER_PLAN):
        print(f"File {DIRECTORIES_TRANSFER_PLAN} not detected. The program has created an empty file.")
        with open(DIRECTORIES_TRANSFER_PLAN, 'w') as f:
            pass
        return []
    with open(DIRECTORIES_TRANSFER_PLAN, 'r') as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            print(f"ERROR reading {DIRECTORIES_TRANSFER_PLAN}: {e}")
            return []

def connect_ftp():
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USERNAME, FTP_PASSWORD)
        print("FTP server is connected.")
        return ftp
    except Exception as e:
        print(f"ERROR connecting to FTP server: {e}")
        return None

def ensure_remote_directory(ftp, remote_dir):
    """Creates directories recursively if they don't exist."""
    
    if remote_dir.startswith('./') or remote_dir.startswith('../'):
        print(f"Detected relative path. Please use an absolute path. '{remote_dir}' will not be created")
        return

    dirs = remote_dir.strip('/').split('/')
    path = ''
    for directory in dirs:
        path += f'/{directory}'
        try:
            ftp.cwd(path)
        except ftplib.error_perm:
            try:
                ftp.mkd(path)
                print(f"Created {path} on the server.")
            except ftplib.error_perm as e:
                if not e.args[0].startswith('550'):
                    print(f"Error creating {path}: {e}")
                    raise
        else:
            print(f"{path} already exists on the server.")

def upload_file(ftp, local_path, remote_path):
    """Upload a file to the server."""
    with open(local_path, 'rb') as f:
        ftp.storbinary(f'STOR {remote_path}', f)
    print(f"Uploaded {local_path} to {remote_path}")

def upload_directory(ftp, local_dir, remote_dir):
    """Recursively upload a directory to the server."""
    for root, dirs, files in os.walk(local_dir):
        rel_path = os.path.relpath(root, local_dir)
        rel_path = '' if rel_path == '.' else rel_path
        current_remote_dir = os.path.join(remote_dir, rel_path).replace('\\', '/')
        
        # Creating directory
        try:
            ensure_remote_directory(ftp, current_remote_dir)
        except Exception as e:
            print(f"ERROR creating directory {current_remote_dir} on server: {e}")
            continue
        
        # Uploading files
        for file in files:
            local_file = os.path.join(root, file)
            remote_file = f"{current_remote_dir}/{file}"
            try:
                upload_file(ftp, local_file, remote_file)
            except Exception as e:
                print(f"ERROR uploading file: {local_file}: {e}")

def begin_uploading_process(transfer_plan):
    ftp = connect_ftp()
    if not ftp:
        return
    try:
        for item in transfer_plan:
            client_dir = item["ClientDirectory"]
            server_dir = item["ServerDirectory"]
            if not os.path.exists(client_dir):
                print(f"Local directory does not exist: {client_dir}")
                continue
            create_auto_remove_file(client_dir)
            try:
                ensure_remote_directory(ftp, server_dir)
            except Exception as e:
                print(f"ERROR: can't create {server_dir} on the server: {e}")
                continue
            upload_directory(ftp, client_dir, server_dir)
            print(f"Directory uploaded: {client_dir} to {server_dir} on the server.")

            # Updating downloaded directories list on server
            try:                
                update_download_list_on_server(ftp, server_dir)
            except Exception as e:
                print(f"ERROR: can't update download list on server: {REMOTE_DOWNLOADED_DIRECTORIES_FILE}: {e}")

            # Visual delimiter
            print(f"\n{'='*20}\n")
    finally:
        ftp.quit()

def update_download_list_on_server(ftp, server_dir):
    local_downloaded_directories_file = "temp_downloaded_directories.txt"
    if not os.path.exists(local_downloaded_directories_file):
            with open(local_downloaded_directories_file, 'w') as f:
                pass

    # Download list
    with open(local_downloaded_directories_file, 'wb') as f:
        ftp.retrbinary(f'RETR {REMOTE_DOWNLOADED_DIRECTORIES_FILE}', f.write)
    
    # Add new directories
    with open(local_downloaded_directories_file, 'a') as f:
        f.write(server_dir + '\n')
    
    # Upload updated list
    with open(local_downloaded_directories_file, 'rb') as f:
        upload_file(ftp, local_downloaded_directories_file, REMOTE_DOWNLOADED_DIRECTORIES_FILE)
    os.remove(local_downloaded_directories_file)
    print(f"Added {server_dir} to {REMOTE_DOWNLOADED_DIRECTORIES_FILE}")

def download_file(ftp, remote_path, local_path):
    """Download a single file from the server."""
    with open(local_path, 'wb') as f:
        ftp.retrbinary(f'RETR {remote_path}', f.write)
    print(f"Downloaded {remote_path} to {local_path}")

def download_directory_recursively(ftp, remote_dir, local_dir):
    """Recursively download a directory from the server."""
    os.makedirs(local_dir, exist_ok=True)
    ftp.cwd(remote_dir)
    items = []
    ftp.retrlines('LIST', items.append)
    for item in items:
        parts = item.split()
        name = parts[-1]
        if item.lower().startswith('d'):
            download_directory_recursively(ftp, f"{remote_dir}/{name}", os.path.join(local_dir, name))
        else:
            download_file(ftp, f"{remote_dir}/{name}", os.path.join(local_dir, name))

def load_downloaded_directories(ftp):
    """Download the directories list."""
    local_downloaded = "temp_downloaded_directories.txt"
    try:
        with open(local_downloaded, 'wb') as f:
            ftp.retrbinary(f'RETR {REMOTE_DOWNLOADED_DIRECTORIES_FILE}', f.write)
        with open(local_downloaded, 'r') as f:
            directories = [line.strip() for line in f if line.strip()]
        os.remove(local_downloaded)
        return directories
    except ftplib.error_perm as e:
        if str(e).startswith('550'):
            with open(local_downloaded, 'w') as f:
                pass
            with open(local_downloaded, 'rb') as f:
                ftp.storbinary(f'STOR {REMOTE_DOWNLOADED_DIRECTORIES_FILE}', f)
            os.remove(local_downloaded)
            return []
        else:
            print(f"ERROR: Can't download {REMOTE_DOWNLOADED_DIRECTORIES_FILE}: {e}")
            return []

def update_auto_remove_files():
    ftp = connect_ftp()
    if not ftp:
        return
    try:
        directories = load_downloaded_directories(ftp)
        current_time = datetime.now(UTC)
        for directory in directories:
            auto_remove_remote = f"{directory}/auto_remove.json"
            auto_remove_local = "temp_auto_remove.json"
            # Download existing file
            try:
                ftp.retrbinary(f'RETR {auto_remove_remote}', open(auto_remove_local, 'wb').write)
                with open(auto_remove_local, 'r') as f:
                    data = json.load(f)
                data["last_sync_time"] = (current_time + timedelta(seconds=AUTO_REMOVE_FILES_SYNC_TIME_STEP_SECONDS)).isoformat()
            except ftplib.error_perm as e:
                if str(e).startswith('550'):
                    # File does not exist, create a new one
                    data = {
                        "creation_time": current_time.isoformat(),
                        "last_sync_time": (current_time + timedelta(seconds=AUTO_REMOVE_FILES_SYNC_TIME_STEP_SECONDS)).isoformat()
                    }
                else:
                    print(f"Error downloading {auto_remove_remote}: {e}")
                    continue
            except json.JSONDecodeError as e:
                print(f"Error reading {auto_remove_remote}: {e}")
                continue
            # Save the updated file
            with open(auto_remove_local, 'w') as f:
                json.dump(data, f, indent=4)
            try:
                ftp.storbinary(f'STOR {auto_remove_remote}', open(auto_remove_local, 'rb'))
                print(f"{current_time}: Updated file {auto_remove_remote} on the server.")
            except Exception as e:
                print(f"Error writing {auto_remove_remote}: {e}")
            finally:
                os.remove(auto_remove_local)
        # Deleting local auto_remove.json files
        transfer_plan = load_transfer_plan()
        for item in transfer_plan:
            client_dir = item["ClientDirectory"]
            auto_remove_path = os.path.join(client_dir, "auto_remove.json")
            if os.path.exists(auto_remove_path):
                os.remove(auto_remove_path)
                print(f"Deleted local file {auto_remove_path}.")
    finally:
        ftp.quit()

def initial_upload():
    transfer_plan = load_transfer_plan()
    if not transfer_plan:
        print("No directories to transfer. Exiting.")
        return
    begin_uploading_process(transfer_plan)

def schedule_sync():
    schedule.every(AUTO_REMOVE_FILES_SYNC_TIMER_SECONDS).seconds.do(update_auto_remove_files)
    print(f"Scheduled synchronization every {AUTO_REMOVE_FILES_SYNC_TIMER_SECONDS} seconds.")
    while True:
        schedule.run_pending()
        time.sleep(1)

def print_start_info():
    print(
f"""
REQUIRED FILE: {DIRECTORIES_TRANSFER_PLAN}
CONTENT EXAMPLE: 
'
[
    {{
        "ClientDirectory": "C:\\DirectoryToMove",
        "ServerDirectory": "/home/ftpuser/upload/DirectoryToMove"
    }}
]
'
PS: use absolute paths in this file!
""")

def main():
    print_start_info()
    initial_upload()
    schedule_sync()

if __name__ == "__main__":
    main()
