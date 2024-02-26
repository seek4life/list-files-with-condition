import os
import sys
import glob
from pathlib import Path
import json
import ast

def generate_paths(modified_files, extension, condition, fixed_modified_files):
    paths = []

    for file_path in modified_files:
        directory = os.path.dirname(file_path)
        base_file_name = os.path.basename(file_path)

        if base_file_name in condition:
            for rule in condition[base_file_name]:
                new_path = os.path.join(directory, rule, extension)
                paths.append(new_path)

    for fixed_file in fixed_modified_files:
        paths.append(fixed_file)

    return paths

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
