## Rules

- Each folder and file in the root folder should be described 

- Description is added after # sign after the folder or file name

- All descriptions in an ASCII diagram should be equaly idented from the begining of the row. The identation should be the number of symbols in the longest ASCII row in the diagram + 2 symbols 

- Each ASCII diagram should contain the direct content of a folder and one level below. The next levels should be described as separate ASCII diagrams

- Each ASCII diagram starts with the root folder and relative path to the respective folder described. For example the first row in the ASCII diagram should be:
`repo-root/` in case the diagram describes the repo root
`repo-root/.rdd-instance/` in case the diagram describes a subfolder in `.rdd-instance/` folder

- Use the following symbols to depict the identation in the ASCII diagram of the folder structure:
├ ─ └ │

- After each ASCII diagram make a summarized description of each file in the described folder. Do not describe the files in subfolders - they will be described in the respective subfolder part.

## Examples


### Example for Root Folder Structure

repo-root/
├── .github/
│   └── prompts/                   # GitHub prompt files
├── .rdd                           # RDD framework folder
│   ├── conventions/               # Format and meaning definitions
│   ├── docs/                      # User guides 
│   ├── prompt-snippets/           # Building blocks for AI prompts
│   ├── src/                   # Python, shell and other code
│   ├── templates/                 # Seed iles to be copy-pasted
│   └── README.md                  # Overview of RDD
└── .rdd-instance/                 # RDD files related to the specific repo
    ├── archive/                   # Previous iterations
    ├── specifications/            # Domain specific detailed specifications
    └── workdir/                   # Current iteration work files


### Examples for Subfolder Structure

repo-root/.github/
└── prompts/
    └── rdd.execute.prompt.md  # Execute command - the only GitHub prompt in RDD


repo-root/.rdd-instance/
└── specifications/                       
    ├── files-and-folders.md              # Description of the repo organization
    └── technical-design.json             # Main technical parameters of the product


 ### Example of file description

**File name**: files-and-folders.md
**Path**: `repo-root/.rdd-instance/specifications/files-and-folders.md`
**Type**: markdown
**Last reviewed**: `20251215-0955`
**Description**: A catalogue of the fies and folders in the repository and their descriptions.
