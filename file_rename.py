import os

def rename_files(folder_path, new_prefix='crall_', start_index=1):
    # Get the list of files in the folder
    files = os.listdir(folder_path)

    # Sort the files to maintain the order
    files.sort()

    # Counter for generating new names
    index = start_index

    for old_name in files:
        # Construct the new name
        new_name = f"{new_prefix}{index}.jpg"

        # Full paths for old and new names
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(old_path, new_path)

        # Increment the counter
        index += 1

# Example usage:
folder_path = "/data/ephemeral/home/data/crall/img/test"
rename_files(folder_path)