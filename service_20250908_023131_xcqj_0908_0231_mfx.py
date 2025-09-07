# 代码生成时间: 2025-09-08 02:31:31
# folder_structure_organizer.py
# This script organizes the folder structure according to predefined rules.

import os
import shutil
def organize_folder_structure(source_path, destination_path, rules):
    """
    Organize the folder structure based on predefined rules.

    :param source_path: The path to the directory to be organized.
    :param destination_path: The path to the directory where files will be organized.
    :param rules: A dictionary with file extensions as keys and
                  the corresponding folder name as values.
    """
    # Check if source and destination paths are directories
    if not os.path.isdir(source_path):
        raise ValueError(f"The source path '{source_path}' is not a directory.")
    if not os.path.isdir(destination_path):
        raise ValueError(f"The destination path '{destination_path}' is not a directory.")

    # Iterate through each file in the source directory
    for filename in os.listdir(source_path):
        filepath = os.path.join(source_path, filename)

        # Check if it's a file and not a directory
        if os.path.isfile(filepath):
            # Get the file extension
            _, file_extension = os.path.splitext(filename)

            # Find the corresponding destination folder based on the file extension
            folder_name = rules.get(file_extension.lower(), 'others')
            folder_path = os.path.join(destination_path, folder_name)

            # Create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Move the file to the destination folder
            try:
                shutil.move(filepath, folder_path)
                print(f"Moved '{filename}' to '{folder_path}'")
            except Exception as e:
                print(f"Error moving '{filename}': {e}")
def main():
    # Define the rules for organizing files
    rules = {
        '.jpg': 'photos',
        '.png': 'photos',
        '.jpeg': 'photos',
        '.mp3': 'music',
        '.mp4': 'videos',
        '.txt': 'documents',
        '.pdf': 'documents',
        '.doc': 'documents',
        '.docx': 'documents'
    }

    # Define the source and destination paths
    source_path = input("Enter the source directory path: ")
    destination_path = input("Enter the destination directory path: ")

    # Call the function to organize the folder structure
    try:
        organize_folder_structure(source_path, destination_path, rules)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()