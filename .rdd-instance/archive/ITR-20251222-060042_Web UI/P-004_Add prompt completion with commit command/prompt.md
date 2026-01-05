A new user requirement: Need to be added action for making a git commit with the changes during the current prompt. The message of the git commit should be the iteration-id + underscore + prompt id + underscore + prompt title. The action will be executed by the user manually and independently from the other actions.


## Modification 01

Execution of `.rdd/src/rdd.py` without arguiments return error. Troubleshoot and fix it.

## Modification 02

When execute `.rdd/src/rdd.py` some of the commands in the menu expect parameters. But the menu tries to execute them without parameters and they fail. Add functionality the user to be asked for input of the parameters. 