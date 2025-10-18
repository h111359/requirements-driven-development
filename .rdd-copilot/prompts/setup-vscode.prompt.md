# Role: 

You are a web developer.

# Context:

C01: I have made some changes in /README.md. The file /web/ai-day-2025.html was created from a previous version of the same README file which now is changed.

# Steps you should execute:
 
I01: Check if `.vscode` folder exists. If not - proceed with the following steps.

I02:  If not exists - create `.vscode` folder

I03: If not exists file: `.vscode/settings.json`, copy in `.vscode/` folder the file `.rdd-copilot/templates/vscode-settings.json`

I04: Read and show the content of `.vscode/settings.json`. Show it to the user. 

I05: Find existing color tags in `.vscode/settings.json` (for example "#3A6EA5"). Choose other colors from a random color theme. For example check [https://colorhunt.co/](https://colorhunt.co/). Ask user for confirmation. 

4. Update the colors in the file `.vscode/settings.json` with the new chosen colors.


# Rules:

R01: Make sure the colors are valid hex color codes. 

R02: Chose colors that are harmonious and visually appealing. 

R03: The color for "titleBar.inactiveBackground" should be a darker shade of the "titleBar.activeBackground" color.
