import os
import sys
import shutil
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def copy_folder_contents(source_folder, destination_folder):
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        messagebox.showwarning("Warning", f"\nSource folder '{source_folder}' does not exist.\n")
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
                    messagebox.showwarning("Warning", f"Directory '{destination_item}' is newer than the source. Aborting copy.\n")
                    return
            shutil.copytree(source_item, destination_item, dirs_exist_ok=True)
        else:
            # Check modification times of files
            if os.path.exists(destination_item):
                source_mtime = os.path.getmtime(source_item)
                destination_mtime = os.path.getmtime(destination_item)
                if destination_mtime > source_mtime:
                    messagebox.showwarning("Warning", f"File '{destination_item}' is newer than the source. Aborting copy.")
                    return
            # Copy files
            shutil.copy2(source_item, destination_item)

    messagebox.showinfo("Done", f"All contents from '{source_folder}' have been copied to '{destination_folder}'.")

def read_variables_from_json(filename):
    # Read user defined folders from json-file
    with open(filename, 'r') as file:
        try:
            data = json.load(file)
        except ValueError:
            messagebox.showerror("Error", "Encoding error in config.json. Remember to use forward slash instead of back slash in the filepaths.")
        try:
            localvariable = data.get('local')
            cloudvariable = data.get('cloud')
            if localvariable is None or cloudvariable is None:
                raise ValueError(messagebox.showerror("Error", "The file config.json does not contain the required variables."))
        except:
            sys.exit()
    return localvariable, cloudvariable


# Function for save button
def button_backup():
    copy_folder_contents(local, cloud)

# Function for restore button
def button_restore():
    copy_folder_contents(cloud, local)

# Function for quit button
def button_quit():
    sys.exit()

# Create main window
root = tk.Tk()
root.title("Cloudsave")

# Create label
local, cloud = read_variables_from_json('config.json')
label_text = f" Local folder: {local}  \n Cloud folder: {cloud}  "
label = tk.Label(root, text=label_text, anchor='w', justify='left')
label.pack(pady=10, fill='x')

# Create frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create buttons and add them to the frame
button1 = tk.Button(button_frame, text="Save to cloud", command=button_backup)
button1.pack(side=tk.LEFT, padx=5)

button2 = tk.Button(button_frame, text="Copy from cloud", command=button_restore)
button2.pack(side=tk.LEFT, padx=5)

button3 = tk.Button(button_frame, text="Quit", command=button_quit)
button3.pack(side=tk.LEFT, padx=5)

# Start the main event loop
root.mainloop()