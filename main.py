import os
import sys
import glob
from pathlib import Path
import json
import ast

def get_folders_up_to_root(path):
    folders = []
    while True:
        folders.append(path)
        if path == os.path.dirname(path):
            break
        path = os.path.dirname(path)
    
    return folders

def find_files(directory, filename):
    file_list = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file == filename:
                file_list.append(os.path.join(root, file))

    return file_list

def generate_paths(modified_files, extension, condition, fixed_modified_files):
    paths = list()

    for file_path in modified_files:
        directory = os.path.dirname(file_path)
        base_file_name = os.path.basename(file_path)
        try:
            found_files = find_files(get_folders_up_to_root(os.path.dirname(file_path))[-2],extension)
        except IndexError:
            return fixed_modified_files

        if base_file_name in condition:
            for rule in condition[base_file_name]:
                for file in found_files:
                    if rule in file:
                        paths.append(file)

    for fixed_file in fixed_modified_files:
        paths.append(fixed_file)

    return list(set(paths))

def main():
    modified_file = ast.literal_eval(os.environ["INPUT_MODIFIED_FILE"])
    extension = os.environ["INPUT_EXT"]
    try:
        condition = json.loads(os.environ["INPUT_CONDITION"])
    except json.decoder.JSONDecodeError as err:
        print("ERROR: Format error in passing the condition variable, check for quotes in",os.environ["INPUT_CONDITION"],": \n", err)
    fixed_modified_files = json.loads(os.environ["INPUT_FIXED_MOD_FILES"])

    print("INFO: INPUTS Provided:\n")
    print("modified_file:",modified_file)
    print("\nextension:",extension)
    print("\ncondition:",condition)
    print("\nfixed_modified_files:",fixed_modified_files,"\n")
    output_paths = generate_paths(modified_file, extension, condition, fixed_modified_files)

    # Print the result
    print("paths", output_paths)
    
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        print(f'paths={output_paths}\n', file=f)
    print("INFO: The final paths",output_paths)
    sys.exit(0)

if __name__ == "__main__":
    main()
