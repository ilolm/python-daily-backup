#!/usr/bin/env python3

import datetime
import os
import glob

# Backup configuration
file_to_backup = "/root/handbook.docx"
backup_folder = '/media/BackupDrive/handbook/'
script_file_name = "handbook_backup.py"
max_backups = 10

def read_file():
    global file_to_backup

    with open(file_to_backup, 'rb') as handbook:
        return handbook.read()

def write_file(data):
    time = datetime.datetime.now()
    backup_filename = "backup_{:02d}-{:02d}_{:02d}:{:02d}:{:02d}.docx".format(
        time.day, time.month, time.hour, time.minute, time.second
    )
    backup_path = os.path.join(backup_folder, backup_filename)

    with open(backup_path, 'wb') as handbook_backup:
        handbook_backup.write(data)
    print(f"Backup created: {backup_path}")

def clean_old_backups():
    global script_file_name

    # Get a list of all backup files in the directory, sorted by modification time (oldest first)
    backups = sorted(
        glob.glob(os.path.join(backup_folder, "backup_*.docx")),
        key=os.path.getmtime
    )

    # Ensure that the backup script itself is not included in the list
    backups = [f for f in backups if os.path.basename(f) != [script_file_name]

    # If there are more backups than max_backups, delete the oldest ones
    if len(backups) > max_backups:
        for backup_to_delete in backups[:-max_backups]:
            os.remove(backup_to_delete)
            print(f"Deleted old backup: {backup_to_delete}")

def main():
    handbook_data = read_file()
    write_file(handbook_data)
    clean_old_backups()

if __name__ == "__main__":
    main()
