import os
import json
import shutil
from pathlib import Path

from utils import get_keys

def dir_serach(filename):
    """Searches for a file with the given filename in the current directory and its subdirectories."""
    current_dir = str(Path.cwd())
    for root, dirs, files in os.walk(current_dir):
        if filename in files:
            file_path = os.path.join(root, filename)
            return file_path, filename
    return None, None 

def update(file, existing_content):
    """Updates the specified file with the provided content."""
    file.seek(0)
    json.dump(existing_content, file, indent=4)
    file.truncate()

def create_or_edit_file(filename, content="", edit=False,defult=True):
    """Creates or edits a file with the given filename and writes the specified content to it.
    If a file with the same name exists and edit=False, appends a unique number to the filename."""
    try:
        user = get_keys()[0]
        current_dir = str(Path.cwd())
        root = os.path.join(current_dir, user["directory"])
        os.makedirs(root, exist_ok=True)
        
        if not edit:
            base_filename, file_extension = os.path.splitext(filename)
            counter = 1
            new_filename = filename
            while os.path.exists(os.path.join(root, new_filename)):
                new_filename = f"{base_filename}_{counter}{file_extension}"
                counter += 1
        else:
            new_filename = filename
        if defult:
            
            with open(os.path.join(root, new_filename), 'w') as file:
                json.dump(content, file, indent=4)
        else:
            with open(new_filename, 'w') as file:
                json.dump(content, file, indent=4)
        print(f"File '{new_filename}' has been created/edited successfully.")
        return root, new_filename
    except Exception as e:
        print(f"An error occurred while creating/editing the file: {e}")


def append_to_file(filename, content):
    """Appends the specified content to the file with the given filename."""
    user = get_keys()[0]
    current_dir = str(Path.cwd())
    root = os.path.join(current_dir, user["directory"])
    os.makedirs(root, exist_ok=True)

    # Check if file exists, create it if it doesn't
    if not os.path.exists(os.path.join(root, filename)):
        create_or_edit_file(filename, content)

    try:
        # Read existing content
        with open(os.path.join(root, filename), 'r') as file:
            existing_content = json.load(file)

        # Check if the existing content is a list or a dict
        if isinstance(existing_content, list):
            # If existing content is a list, append the new content
            if isinstance(content, list):
                existing_content.extend(content)  # Assuming 'content' is also a list
            else:
                raise ValueError("Cannot append non-list content to a list")

        elif isinstance(existing_content, dict):
            # If existing content is a dict, update it
            if isinstance(content, dict):
                existing_content.update(content)  # Assuming 'content' is a dict
            else:
                raise ValueError("Content must be a dictionary to update existing dictionary")

        # Write the updated content back to the file
        with open(os.path.join(root, filename), 'w') as file:
            json.dump(existing_content, file, indent=4)

    except Exception as e:
        print(f"An error occurred while appending to the file: {e}")




def read_file(filename):
    """Reads the content of the file with the given filename and returns it."""
    current_dir = str(Path.cwd())
    for root, dirs, files in os.walk(current_dir):
        if filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as file:
                return json.load(file)


def backup_file(file_path):
    """Creates a backup of the file at the specified file path."""
    backup_dir = os.path.join(Path.cwd(), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, os.path.basename(file_path))
    shutil.copy(file_path, backup_path)
    print(f"Backup of '{file_path}' created at '{backup_path}'")

def check_and_restore_important_file(filename, default_content):
    """Checks if an important file is missing and restores it from backup or recreates it with default content."""
    current_dir = str(Path.cwd())
    file_path = os.path.join(current_dir, filename)

    if not os.path.exists(file_path):
        print(f"'{filename}' is missing! Attempting to restore...")

        backup_dir = os.path.join(current_dir, "backups")
        backup_path = os.path.join(backup_dir, filename)

        if os.path.exists(backup_path):
            shutil.copy(backup_path, file_path)
            print(f"'{filename}' restored from backup.")
        else:
            with open(file_path, 'w') as file:
                json.dump(default_content, file, indent=4)
            print(f"'{filename}' was recreated with default content.")
