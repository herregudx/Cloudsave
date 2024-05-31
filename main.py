import os
import shutil
import json
from datetime import datetime


def copy_folder_contents(source_folder, destination_folder):
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"\nSource folder '{source_folder}' does not exist.\n")
        return

    # Ensure the destination folder exists, create it if not
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate over all the files and directories in the source folder
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        destination_item = os.path.join(destination_folder, item)

        if os.path.isdir(source_item):
            # Recursively copy directories
            if os.path.exists(destination_item):
                # Check modification times of directories
                source_mtime = os.path.getmtime(source_item)
                destination_mtime = os.path.getmtime(destination_item)
                if destination_mtime > source_mtime:
                    print(f"\nDirectory '{destination_item}' is newer than the source. Aborting copy.\n")
                    return
            shutil.copytree(source_item, destination_item, dirs_exist_ok=True)
        else:
            # Check modification times of files
            if os.path.exists(destination_item):
                source_mtime = os.path.getmtime(source_item)
                destination_mtime = os.path.getmtime(destination_item)
                if destination_mtime > source_mtime:
                    print(f"\nFile '{destination_item}' is newer than the source. Aborting copy.\n")
                    return
            # Copy files
            shutil.copy2(source_item, destination_item)

    print(f"\nAll contents from '{source_folder}' have been copied to '{destination_folder}'.\n")


def read_variables_from_json(filename):
    # Read user defined folders from json-file
    with open(filename, 'r') as file:
        data = json.load(file)
        localvariable = data.get('local')
        cloudvariable = data.get('cloud')
        if localvariable is None or cloudvariable is None:
            raise ValueError("The JSON file does not contain the required variables.")
    return localvariable, cloudvariable


def menu():
    print("\nLocal folder: " + local + "\nCloud folder: " + cloud)
    userchoice = input("\n[B]ackup to cloud     [R]estore from cloud      [Q]uit\nYour choice: ")
    if userchoice.upper() == "B":
        copy_folder_contents(local, cloud)
    elif userchoice.upper() == "R":
        copy_folder_contents(cloud, local)
    elif userchoice.upper() == "Q":
        exit()


if __name__=="__main__": 
    local, cloud = read_variables_from_json('filepaths.json')
    menu()
