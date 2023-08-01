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
    folder_map = json.loads(os.environ["INPUT_FOLDER_MAP"])

    paths = ''
    print(modified_file,folder_map)

    for modfile in list(modified_file):
        for rule_file,rule_folder in folder_map.items():
            if os.path.basename(modfile) == rule_file:
                for root, dirs, files in os.walk(os.path.dirname(modfile)):
                    for file in files:
                        if file.endswith(f'{extension}'):
                            for rule in rule_folder:
                                if path_contains_directory(root, rule):
                                    paths = paths + '\"' + root + '/' + str(file) + '\", '

    paths = remove_last_occurrence(paths, ',')
    paths = "[" + paths + "]"
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        print(f'paths={paths}\n', file=f)
    print(paths)

    sys.exit(0)


if __name__ == "__main__":
    main()
