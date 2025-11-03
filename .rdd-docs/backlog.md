## Project Backlog
This file defines user stories, features, and tasks for GitHub Copilot to use as development context.


## Issues

### Issue 4: Add gitignore

#### Overview:

**Status:** CLOSED
**Created by:** h111359
**Created at:** 2025-10-31

#### Description (first comment):

> ## What:
> 
> Appropriate to the repo content .gitignore file to be added.
> 
> ## Why:
> 
> To be avoided unnecessary tracking of files which are not contributing to the main code > of the repo
> 
> ## Acceptance Criteria:
> 
> - The whole repo and all the files in it (main branch) should be revised so to be well > understood the repo structure and meaning
> - .gitignore file to be created in the root folder of the repo
> - gitignore to follow the best practices, still to be avoided unnecessary complexity
> - .github, .vscode and .rdd should not be excluded
> - The development to be made in a separate fix branch named as per the specified in .> rdd-docs/version-control.md
> - PR with added .gitignore file 


### Issue 12: Replace change with enhancement

#### Overview:

**Status:** CLOSED
**Created by:** h111359
**Created at:** 2025-11-02

#### Description (first comment):

> ## What:
>
> I want to stop using "change" as term in RDD and to start using "enhancement" instead. For branches prefixes instead of "feat" should be used "enh".
>
> ## Why:
>
> Enhancement is more popular term and more clearly represent the idea of applying feature/issue/user story.
>
> ## Acceptance Criteria:
>
> - When creating a new branch the possible options to be enhancement and fix
> - the script change-utils.sh should remain with the same name, but to be revised as code and whenever inside is used feat or feature - to be changed to enh/enhancement
> - The file .rdd-docs/requirements.md to be updated with enhancement terminology. To be explained that change = enhncement or fix
> - To be searched all the files in .github and the terminology to be changed whenever appropriate
> - To be searched all the files in .rdd and the terminology to be changed whenever appropriate
> - To be searched all the files in .rdd-docs and the terminology to be changed whenever appropriate


### Issue 13: journal becomes copilot-prompts

#### Overview:

**Status:** OPEN
**Created by:** h111359
**Created at:** 2025-11-02

#### Description (first comment):

> ## What:
>
> Rename journal.md to copilot-prompts.md
>
> ## Why:
>
> Journal term do not represent the true meaning.
>
> ## Acceptance Criteria
>
> - The template journal.md to be renamed to copilot-prompts.md
> - All the references to journal.md in the files in .github/prompts/, .rdd/scripts/, .rdd/templates, .rdd-docs/ to be changed to copilot-prompts.md


### Issue 18: clarification taxonomy to checklist

#### Overview:

**Status:** OPEN
**Created by:** h111359
**Created at:** 2025-11-02

#### Description (first comment):

> ## What:
>
> Rename `clarity-taxonomy.md` to `clarity-checklist.md`.
>
> ## Why:
>
> The new name better represents the purpose and content of the file.
>
> ## Acceptance Criteria:
>
> - The file `.rdd/templates/clarity-taxonomy.md` is renamed to `.rdd/templates/clarity-checklist.md`.
> - All scripts in `.rdd/scripts` are revised, and all references to `clarity-taxonomy.md` are changed to `clarity-checklist.md`.
> - All files in `.rdd/templates` are revised, and all references to `clarity-taxonomy.md` are changed to `clarity-checklist.md`.
> - All files in `.rdd-docs` or its subfolders (excluding `archive`) are revised, and all references to `clarity-taxonomy.md` are changed to `clarity-checklist.md`.
> - All files in `.github` or its subfolders are revised, and all references to `clarity-taxonomy.md` are changed to `clarity-checklist.md`.


