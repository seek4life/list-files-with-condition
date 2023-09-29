import os
import sys
import glob
from pathlib import Path
import json
import ast

def path_contains_directory(path, directory_name):
    # Split the provided path into its individual components
    path_components = os.path.normpath(path).split(os.path.sep)

    # Check if the specified directory name is in the path components
    return directory_name in path_components

def get_folders_up_to_root(path):
    folders = []
    while True:
        folders.append(path)
        if path == os.path.dirname(path):
            break
        path = os.path.dirname(path)
    
    return folders

def remove_last_occurrence(string: str, char: str):
    length = len(string)
    string2 = ''
    for i in range(length):
        if string[i] == char:
            string2 = string[0:i] + string[i + 1:length]
    return string2


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
    generate_list={}
    if modified_file:
        paths = ''
        for rule_file,rule_folders in condition.items():
            for modfile in list(modified_file):
                if os.path.basename(modfile) == rule_file:
                    generate_list[modfile] = ()
                    folders_up_to_root = get_folders_up_to_root(modfile)
                    for folder in folders_up_to_root:
                         
                         for rule in rule_folders:
                            if os.path.isdir(folder):
                                
                                folders = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]

                                for c_folder in folders:
                                    if c_folder == rule:
                                        f_folder = folder+"/"+rule
                                        files = [f for f in os.listdir(f_folder) if os.path.join(f_folder, f)]
                                        for file in files:
                                            if file.endswith(f'{extension}'): 
                                                generate_list[modfile] = f_folder+"/"+file


        paths = generate_list.values()
        if paths != "":
            
            paths = str(list(set(list(paths) + list(fixed_modified_files))))
    else:
        paths = fixed_modified_files
    
    
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        print(f'paths={paths}\n', file=f)
    print("INFO: The final paths",paths)
    sys.exit(0)

if __name__ == "__main__":
    main()
