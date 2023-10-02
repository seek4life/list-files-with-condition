import os
import sys
import glob
from pathlib import Path
import json
import ast

def list_files_and_folders(root_dir):
    found_files = []
    for root, dirs, files in os.walk(root_dir):
        # for directory in dirs:
        #     folder_path = os.path.join(root, directory)
        #     print(f"Folder: {folder_path}")
        for file in files:
            file_path = os.path.join(root, file)
            found_files.append(file_path)
    return found_files


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
                if os.path.basename(modfile) == rule_file.split('/')[-1]:
                    files_up_to_root = list_files_and_folders(rule_file.split('/')[0])
                    for file in files_up_to_root:
                         for rule in rule_folders:
                            
                            if (rule == file.split('/')[-2]) and (file.endswith(extension)):
                                 print("adding:",file)
                                 generate_list[modfile+file] = file
 
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
