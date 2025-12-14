## Instructions

1. Run the script
   `python .rdd/scripts/rdd.py workspace list-files` which lists all the file, folders and recursively their subfolders and stores the result in `.rdd-instance/workdir/files-list.md` excluding folders and subfolders which start with "." or folders like "venv" in a terminal by running the script:
     ```python
     python .rdd/scripts/rdd.py workspace list-files    
     ```
   
2. Create (or revise if exists) the file `.rdd-instance/workdir/files-analysis.md` and check if there are files in `.rdd-instance/workdir/files-list.md` which are missing or are with newer timestapm of the last change. For those - open the file, read it and add a short summary in `.rdd-instance/workdir/files-analysis.md` containing the relative path, type and only if it is readable - short summary of its content. Group the file entries and order them per folder they are in (same for the folders).

3.  Based on the information in `.rdd-instance/workdir/files-analysis.md` update the content of `.rdd-instance/specifications/files-and-folders.md` section "## Project Folder Structure" considering the current content of  this section only as an example of the format expected and not reflection of the reality (as it could be just an example or to be obsolete already). 

4. Compare the current content of `.rdd-instance/specifications/files-and-folders.md` section "## Project Folder Structure" with the actual folder structure in `.rdd-instance/workdir/files-list.md` and ensure that all files and folders are represented there correctly with their purpose explained. Add missing files/folders, remove obsolete ones, and correct any inaccuracies.