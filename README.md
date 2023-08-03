# List Files Action

<p align="center">

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/seek4life/list-files-action?label=latest-release)](https://github.com/github.com-seek4life:seek4life/list-files-with-condition/releases/latest)

[![Test](https://github.com/github.com-seek4life:seek4life/list-files-with-condition/actions/workflows/test.yml/badge.svg)](https://github.com/github.com-seek4life:seek4life/list-files-with-condition/actions/workflows/test.yml)

</p>
GitHub action to list path of all files of a particular extension in the folder/directory
specified by the user.

## Inputs
| Input                                    | Description                           |
|------------------------------------------|---------------------------------------|
| `repo` (required)                        | Repository name where to search files |
| `ref`  (optional => default is 'master') | Branch or tag to checkout             |
| `modified_file` (required)               | List ofPath where searching files     |
| `ext`  (required)                        | File extension to match               |
| `condition`  (required)                 | list of list containing the conition  |

## Outputs

| Output       | Description                               |
|--------------|-------------------------------------------|
| `paths`      | Paths of all the files with the extension |

## Usage example

```yaml
name: Test

on:
  push:
    tags-ignore:
      - '*'
    branches:
      - 'master'
  pull_request:
  workflow_dispatch:

jobs:
  list-files:
    runs-on: ubuntu-latest
    outputs:
      paths: ${{ steps.list-files.outputs.paths }}
    steps:
      - name: List Files
        id: list-files
        uses: seek4life/list-files-with-condition@v0.0.1
        with:
          repo: ${{ github.repository }}
          ref: ${{ github.ref }}
          path: "."
          ext: ".yml"
          folder_map: '{"testconfigfile.hcl": ["test-folder1","test-folder2"]}'
          fixed_modiified_files: '[]'  # Optional
  Test:
    needs: list-files
    strategy:
      matrix:
        paths: ${{ fromJson(needs.list-files.outputs.paths) }}
    runs-on: ubuntu-latest
    steps:
      - name: Output results
        run: |
          echo ${{ matrix.paths }}
```
Output generated for the above yaml file (in this repository):


## License
[MIT license]

[MIT license]: LICENSE