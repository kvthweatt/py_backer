# Written by Karac Thweatt aka Father Crypto for UTTCex

import time, os, shutil, json

backer_ver = "1.2"

def copy_file(file_path, backup_dir):
    file_name = os.path.basename(file_path)
    shutil.copy2(file_path, os.path.join(backup_dir, file_name))

def monitor_directories(source_dirs, backup_dirs, backup_times):
    file_mod_times = {source_dir: {} for source_dir in source_dirs}
    last_backup_times = {source_dir: 0 for source_dir in source_dirs}

    while True:
        current_time = time.time()
        for index, (source_dir, backup_dir) in enumerate(zip(source_dirs, backup_dirs)):
            delay = int(backup_times.get(str(index), 5))  # default to 5 seconds if not specified
            if current_time - last_backup_times[source_dir] >= delay:
                for filename in os.listdir(source_dir):
                    file_path = os.path.join(source_dir, filename)
                    if os.path.isfile(file_path) and os.path.getmtime(file_path) != file_mod_times[source_dir].get(file_path, 0):
                        file_mod_times[source_dir][file_path] = os.path.getmtime(file_path)
                        copy_file(file_path, backup_dir)
                        print(f"Change Detected!\nFile: \"{filename}\" copied to backup directory: \"{backup_dir}\"")
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
