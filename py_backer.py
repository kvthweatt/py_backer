# Written by Karac Thweatt aka Father Crypto for UTTCex

import time, os, shutil, json

backer_ver = "1.0"

source_dir = ""
backup_dir = ""

def copy_file(file_path):
    file_name = os.path.basename(file_path)
    shutil.copy2(file_path, os.path.join(backup_dir, file_name))

def monitor_directory(source_dir, backup_dir):
    file_mod_times = {}

    while True:
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)
            # Check if file is a regular file and has been modified
            if os.path.isfile(file_path) and os.path.getmtime(file_path) != file_mod_times.get(file_path, 0):
                file_mod_times[file_path] = os.path.getmtime(file_path)
                # Copy the modified file to backup directory
                copy_file(file_path)
                print(f"Change Detected!\nFile: \"{filename}\" copied to backup directory.")
        time.sleep(5)

if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config_file.seek(0)
        data = json.loads(config_file.read())
        proj_name = data["project_name"]
        proj_ver = data["project_version"]
        source_dir = data["source_dir"]
        backup_dir = data["backup_dir"]

    print(f"PyBacker {backer_ver}\nMonitoring project: {proj_name} v{proj_ver}")
    monitor_directory(source_dir, backup_dir)
