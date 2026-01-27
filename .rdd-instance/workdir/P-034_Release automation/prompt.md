Create in the prompt workdir a file release_automation_analysis.md
The file should contain detail analysis of the options during PR to main branch to be executed generation of a new release with the respective needed artefacts attached.
The source of the release version should be `.rdd/config/manifest.json` - framework.version
Check for options to be assigned tag to the release in format for example: v2.1.0
Provide best practices for generation of release notes - where to take them from and how to persist them?
Currently the releases are created in `build` folder by a script `build/build.py`