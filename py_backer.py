# Written by Karac Thweatt aka Father Crypto for UTTCex

import time
import os
import shutil
import json

backer_ver = "1.1"

def copy_file(file_path, backup_dir):
    file_name = os.path.basename(file_path)
    shutil.copy2(file_path, os.path.join(backup_dir, file_name))

def monitor_directories(source_dirs, backup_dirs):
    file_mod_times = {source_dir: {} for source_dir in source_dirs}

    while True:
        for source_dir, backup_dir in zip(source_dirs, backup_dirs):
            for filename in os.listdir(source_dir):
                file_path = os.path.join(source_dir, filename)
                # Check if file is a regular file and has been modified
                if os.path.isfile(file_path) and os.path.getmtime(file_path) != file_mod_times[source_dir].get(file_path, 0):
                    file_mod_times[source_dir][file_path] = os.path.getmtime(file_path)
                    # Copy the modified file to backup directory
                    copy_file(file_path, backup_dir)
                    print(f"Change Detected!\nFile: \"{filename}\" copied to backup directory: \"{backup_dir}\"")
        time.sleep(5)

if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
        proj_name = config_data.get("project_name", "")
        proj_ver = config_data.get("project_version", "")
        source_dirs = [config_data.get("source_dirs", {}).get(str(i), "") for i in range(len(config_data.get("source_dirs", {})))]
        backup_dirs = [config_data.get("backup_dirs", {}).get(str(i), "") for i in range(len(config_data.get("backup_dirs", {})))]

    print(f"PyBacker {backer_ver}\nMonitoring project: {proj_name} v{proj_ver}")
    monitor_directories(source_dirs, backup_dirs)
