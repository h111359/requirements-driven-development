Create a python script `.rdd/src/actions/files_list_csv_refresh.py` which lists all the file, folders and recursively their subfolders and stores the result in `.rdd-instance/specifications/files-list.csv` excluding folders and subfolders which start with "." or folders like "venv" in a terminal. The file should present the data in a tabular way, should be a tab separated and should have the following fields:
- File Name
- Relative Path
- Modification Time
- Description

On every execution of the script:
- Add new files found in the repository, which are not present in `.rdd-instance/specifications/files-list.csv` and fulfill for them the fields "File Name", "Relative Path" and "Last Modification Time"
- For the files with newer modification time - remove the current text in "Description" field (leave it empty) and update the field "Modification Time"
- Delete files from `.rdd-instance/specifications/files-list.csv` which are not present in the repository any more.

Create a python script `.rdd/src/actions/files_list_csv_set_description.py` which receives parameters file-name and relative-path and for the entry with those values in `.rdd-instance/specifications/files-list.csv` applies the content of third parameter description. This script will be called from copilot.