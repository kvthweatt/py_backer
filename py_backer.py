# Written by Karac Thweatt aka Father Crypto for UTTCex

import time, os, shutil, json

backer_ver = "1.3"

def copy_item(item_path, backup_dir):
    item_name = os.path.basename(item_path)
    destination = os.path.join(backup_dir, item_name)
    if os.path.isdir(item_path):
        # Recursively copy the directory
        if os.path.exists(destination):
            shutil.rmtree(destination)
        shutil.copytree(item_path, destination)
    else:
        shutil.copy2(item_path, destination)

def monitor_directories(source_dirs, backup_dirs, backup_times):
    item_mod_times = {source_dir: {} for source_dir in source_dirs}
    last_backup_times = {source_dir: 0 for source_dir in source_dirs}

    while True:
        current_time = time.time()
        for index, (source_dir, backup_dir) in enumerate(zip(source_dirs, backup_dirs)):
            delay = int(backup_times.get(str(index), 5))  # default to 5 seconds if not specified
            if current_time - last_backup_times[source_dir] >= delay:
                for root, dirs, files in os.walk(source_dir):
                    for name in dirs + files:
                        item_path = os.path.join(root, name)
                        rel_path = os.path.relpath(item_path, source_dir)
                        backup_item_path = os.path.join(backup_dir, rel_path)

                        # Check if the item is modified or new
                        if os.path.exists(item_path) and os.path.getmtime(item_path) != item_mod_times[source_dir].get(item_path, 0):
                            item_mod_times[source_dir][item_path] = os.path.getmtime(item_path)
                            # Copy the modified or new item to the backup directory
                            try:
                                copy_item(item_path, os.path.dirname(backup_item_path))
                            except:
                                print(f"Failed to back up {source_dir}{rel_path}")
                                continue
                            print(f"Change Detected!\nItem: \"{rel_path}\" copied to backup directory: \"{backup_dir}\"")
                last_backup_times[source_dir] = current_time
        time.sleep(1)

if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
        proj_name = config_data.get("project_name", "")
        proj_ver = config_data.get("project_version", "")
        source_dirs = [config_data.get("source_dirs", {}).get(str(i), "") for i in range(len(config_data.get("source_dirs", {})))]
        backup_dirs = [config_data.get("backup_dirs", {}).get(str(i), "") for i in range(len(config_data.get("backup_dirs", {})))]
        backup_times = {str(i): config_data.get("backup_times", {}).get(str(i), 5) for i in range(len(config_data.get("source_dirs", {})))}

    print(f"PyBacker {backer_ver}\nMonitoring project: {proj_name} v{proj_ver}")
    monitor_directories(source_dirs, backup_dirs, backup_times)
