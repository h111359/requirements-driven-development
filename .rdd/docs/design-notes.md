## File and Folder Structure

The current RDD folder structure is as follows:

### Root Folder

repo-root/
├── .github/
│   └── prompts/                   # GitHub prompt files
├── .rdd                           # RDD framework folder
│   ├── config/                    # Framework-owned executable configurations
│   ├── conventions/               # Format and meaning definitions
│   ├── docs/                      # User guides 
│   ├── prompt-snippets/           # Building blocks for AI prompts
│   ├── prompt-templates/          # Whole well formed prompts
│   ├── scripts/                   # Python, shell and other code
│   ├── templates/                 # Seed files to be copy-pasted
│   └── README.md                  # Overview of RDD
└── .rdd-instance/                     # RDD files related to the specific repo
    ├── archive/                   # Previous iterations workdir content archives
    ├── specifications/            # Domain specific detailed specifications
    ├── workdir/                 # Current iteration work files
    ├── config.json                # RDD configuration for the current repo
    └── requirements.md            # Current repo requirements file

### GitHub Prompts Folder

/repo-root/.github/
├── prompts/
    └── rdd.execute.prompt.md  # Execute command - the only GitHub prompt in RDD

### Specifications Folder

/repo-root/.rdd-instance/
└── specifications/                       
    ├── architecture-decision-records.md  # Architecture design records catalogue
    ├── components.md                     # Product components and dependencies
    ├── data.md                           # Data structures and worklow
    ├── deployment.md                     # Depoloyement artefacts, CI/CD process
    ├── files-and-folders.md              # Description of the repo organization
    ├── front-end.md                      # User interfaces and visualizations
    ├── infrastructure.md                 # Services, compute, storage, network ...
    ├── quality-assurance.md              # Tests, quality benchmarks, governance 
    ├── security.md                       # Authentication and authorization, protection ...
    └── technical-design.json             # Main technical parameters of the product

### workdir Folder

/repo-root/.rdd-instance/
└── workdir/ 
    ├── work-iteration-prompt.md      # Text of the promt which should be executed
    └── work-iteration-registry.json  # Parameters for execution of the iteration prompt

The aim is to be achieve the most appropriate folder structure both for RDD as a system and RDD as a framework, which is installed and working on other products. Currently RDD has a folder .rdd, where are the static files of the framework and .rdd-instance, where are the current project setup, requirements and conventions, prompts, and archive. One advantage of separation on .rdd and .rdd-instance folder is that during install the folder .rdd is set as just copy-paste from the build file and .rdd-instance is created from templates in .rdd.