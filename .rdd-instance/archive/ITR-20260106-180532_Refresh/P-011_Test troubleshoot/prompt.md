This is the test log from pull request to merge to DEV branch (executing .github/workflows/tests.yml). Find the issues and fix them:

2026-01-07T07:06:25.4644353Z Current runner version: '2.330.0'
2026-01-07T07:06:25.4667328Z ##[group]Runner Image Provisioner
2026-01-07T07:06:25.4668052Z Hosted Compute Agent
2026-01-07T07:06:25.4668509Z Version: 20251211.462
2026-01-07T07:06:25.4669122Z Commit: 6cbad8c2bb55d58165063d031ccabf57e2d2db61
2026-01-07T07:06:25.4669716Z Build Date: 2025-12-11T16:28:49Z
2026-01-07T07:06:25.4670519Z Worker ID: {a1c9dd61-f603-4355-8171-c5f193fdfa6e}
2026-01-07T07:06:25.4671505Z ##[endgroup]
2026-01-07T07:06:25.4672258Z ##[group]Operating System
2026-01-07T07:06:25.4673157Z Microsoft Windows Server 2025
2026-01-07T07:06:25.4674024Z 10.0.26100
2026-01-07T07:06:25.4674698Z Datacenter
2026-01-07T07:06:25.4675683Z ##[endgroup]
2026-01-07T07:06:25.4676535Z ##[group]Runner Image
2026-01-07T07:06:25.4677319Z Image: windows-2025
2026-01-07T07:06:25.4678075Z Version: 20251216.149.1
2026-01-07T07:06:25.4680499Z Included Software: https://github.com/actions/runner-images/blob/win25/20251216.149/images/windows/Windows2025-Readme.md
2026-01-07T07:06:25.4682998Z Image Release: https://github.com/actions/runner-images/releases/tag/win25%2F20251216.149
2026-01-07T07:06:25.4684445Z ##[endgroup]
2026-01-07T07:06:25.4686040Z ##[group]GITHUB_TOKEN Permissions
2026-01-07T07:06:25.4688811Z Contents: read
2026-01-07T07:06:25.4689569Z Metadata: read
2026-01-07T07:06:25.4690208Z Packages: read
2026-01-07T07:06:25.4691004Z ##[endgroup]
2026-01-07T07:06:25.4693651Z Secret source: Actions
2026-01-07T07:06:25.4694580Z Prepare workflow directory
2026-01-07T07:06:25.5121793Z Prepare all required actions
2026-01-07T07:06:25.5169930Z Getting action download info
2026-01-07T07:06:25.7782800Z Download action repository 'actions/checkout@v4' (SHA:34e114876b0b11c390a56381ad16ebd13914f8d5)
2026-01-07T07:06:25.9101807Z Download action repository 'actions/setup-python@v5' (SHA:a26af69be951a213d495a4c3e4e4022e16d87065)
2026-01-07T07:06:26.1887341Z Complete job name: All Tests (Windows)
2026-01-07T07:06:26.3354928Z ##[group]Run actions/checkout@v4
2026-01-07T07:06:26.3355881Z with:
2026-01-07T07:06:26.3356321Z   repository: h111359/requirements-driven-development
2026-01-07T07:06:26.3357013Z   token: ***
2026-01-07T07:06:26.3357359Z   ssh-strict: true
2026-01-07T07:06:26.3357726Z   ssh-user: git
2026-01-07T07:06:26.3358090Z   persist-credentials: true
2026-01-07T07:06:26.3358504Z   clean: true
2026-01-07T07:06:26.3358870Z   sparse-checkout-cone-mode: true
2026-01-07T07:06:26.3359316Z   fetch-depth: 1
2026-01-07T07:06:26.3359670Z   fetch-tags: false
2026-01-07T07:06:26.3360042Z   show-progress: true
2026-01-07T07:06:26.3360403Z   lfs: false
2026-01-07T07:06:26.3360736Z   submodules: false
2026-01-07T07:06:26.3361114Z   set-safe-directory: true
2026-01-07T07:06:26.3361712Z ##[endgroup]
2026-01-07T07:06:26.5167127Z Syncing repository: h111359/requirements-driven-development
2026-01-07T07:06:26.5170246Z ##[group]Getting Git version info
2026-01-07T07:06:26.5172279Z Working directory is 'D:\a\requirements-driven-development\requirements-driven-development'
2026-01-07T07:06:26.6357209Z [command]"C:\Program Files\Git\bin\git.exe" version
2026-01-07T07:06:27.0939281Z git version 2.52.0.windows.1
2026-01-07T07:06:27.1001606Z ##[endgroup]
2026-01-07T07:06:27.1026121Z Temporarily overriding HOME='D:\a\_temp\7ae2e0aa-61fc-4133-905f-e3000e284052' before making global git config changes
2026-01-07T07:06:27.1027470Z Adding repository directory to the temporary git global config as a safe directory
2026-01-07T07:06:27.1041935Z [command]"C:\Program Files\Git\bin\git.exe" config --global --add safe.directory D:\a\requirements-driven-development\requirements-driven-development
2026-01-07T07:06:27.1702287Z Deleting the contents of 'D:\a\requirements-driven-development\requirements-driven-development'
2026-01-07T07:06:27.1709454Z ##[group]Initializing the repository
2026-01-07T07:06:27.1719514Z [command]"C:\Program Files\Git\bin\git.exe" init D:\a\requirements-driven-development\requirements-driven-development
2026-01-07T07:06:27.2680096Z Initialized empty Git repository in D:/a/requirements-driven-development/requirements-driven-development/.git/
2026-01-07T07:06:27.2726497Z [command]"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/h111359/requirements-driven-development
2026-01-07T07:06:27.3343337Z ##[endgroup]
2026-01-07T07:06:27.3344411Z ##[group]Disabling automatic garbage collection
2026-01-07T07:06:27.3352796Z [command]"C:\Program Files\Git\bin\git.exe" config --local gc.auto 0
2026-01-07T07:06:27.3637355Z ##[endgroup]
2026-01-07T07:06:27.3638416Z ##[group]Setting up auth
2026-01-07T07:06:27.3650775Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp core\.sshCommand
2026-01-07T07:06:27.3942453Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "sh -c \"git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :\""
2026-01-07T07:06:28.9987796Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-01-07T07:06:29.0267471Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "sh -c \"git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :\""
2026-01-07T07:06:29.5520884Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-01-07T07:06:29.5800507Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "git config --local --show-origin --name-only --get-regexp remote.origin.url"
2026-01-07T07:06:30.1070820Z [command]"C:\Program Files\Git\bin\git.exe" config --local http.https://github.com/.extraheader "AUTHORIZATION: basic ***"
2026-01-07T07:06:30.1393690Z ##[endgroup]
2026-01-07T07:06:30.1394483Z ##[group]Fetching the repository
2026-01-07T07:06:30.1410922Z [command]"C:\Program Files\Git\bin\git.exe" -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +33f4d354b9c61f5e7d957054f6759bc2f85f13f5:refs/remotes/pull/81/merge
2026-01-07T07:06:31.3799607Z From https://github.com/h111359/requirements-driven-development
2026-01-07T07:06:31.3800443Z  * [new ref]         33f4d354b9c61f5e7d957054f6759bc2f85f13f5 -> pull/81/merge
2026-01-07T07:06:31.4082656Z ##[endgroup]
2026-01-07T07:06:31.4083225Z ##[group]Determining the checkout info
2026-01-07T07:06:31.4085672Z ##[endgroup]
2026-01-07T07:06:31.4096834Z [command]"C:\Program Files\Git\bin\git.exe" sparse-checkout disable
2026-01-07T07:06:31.4623736Z [command]"C:\Program Files\Git\bin\git.exe" config --local --unset-all extensions.worktreeConfig
2026-01-07T07:06:31.4941102Z ##[group]Checking out the ref
2026-01-07T07:06:31.4952681Z [command]"C:\Program Files\Git\bin\git.exe" checkout --progress --force refs/remotes/pull/81/merge
2026-01-07T07:06:31.6144831Z ##[error]error: unable to create file .rdd-instance/archive/ITR-20251222-060042_Web UI/P-045_Bug questionnaire-generated and questionnaire-answered flags are set to true immediately after creation of new prompt/modification-001-implementation.md: Filename too long
2026-01-07T07:06:31.6153661Z ##[error]error: unable to create file .rdd-instance/archive/ITR-20251222-060042_Web UI/P-045_Bug questionnaire-generated and questionnaire-answered flags are set to true immediately after creation of new prompt/modification-001.md: Filename too long
2026-01-07T07:06:31.6156384Z ##[error]error: unable to create file .rdd-instance/archive/ITR-20251222-060042_Web UI/P-045_Bug questionnaire-generated and questionnaire-answered flags are set to true immediately after creation of new prompt/modification-002-implementation.md: Filename too long
2026-01-07T07:06:31.6158869Z ##[error]error: unable to create file .rdd-instance/archive/ITR-20251222-060042_Web UI/P-045_Bug questionnaire-generated and questionnaire-answered flags are set to true immediately after creation of new prompt/modification-002.md: Filename too long
2026-01-07T07:06:31.6162300Z ##[error]error: unable to create file .rdd-instance/archive/ITR-20251222-060042_Web UI/P-045_Bug questionnaire-generated and questionnaire-answered flags are set to true immediately after creation of new prompt/modifications-log.json: Filename too long
2026-01-07T07:06:31.6164720Z ##[error]error: unable to create file .rdd-instance/archive/ITR-20251222-060042_Web UI/P-045_Bug questionnaire-generated and questionnaire-answered flags are set to true immediately after creation of new prompt/questionnaire.json: Filename too long
2026-01-07T07:06:31.7161722Z Note: switching to 'refs/remotes/pull/81/merge'.
2026-01-07T07:06:31.7162201Z 
2026-01-07T07:06:31.7162527Z You are in 'detached HEAD' state. You can look around, make experimental
2026-01-07T07:06:31.7163262Z changes and commit them, and you can discard any commits you make in this
2026-01-07T07:06:31.7164330Z state without impacting any branches by switching back to a branch.
2026-01-07T07:06:31.7164914Z 
2026-01-07T07:06:31.7165296Z If you want to create a new branch to retain commits you create, you may
2026-01-07T07:06:31.7166091Z do so (now or later) by using -c with the switch command. Example:
2026-01-07T07:06:31.7166519Z 
2026-01-07T07:06:31.7166702Z   git switch -c <new-branch-name>
2026-01-07T07:06:31.7167000Z 
2026-01-07T07:06:31.7167141Z Or undo this operation with:
2026-01-07T07:06:31.7167404Z 
2026-01-07T07:06:31.7167525Z   git switch -
2026-01-07T07:06:31.7167712Z 
2026-01-07T07:06:31.7168054Z Turn off this advice by setting config variable advice.detachedHead to false
2026-01-07T07:06:31.7168599Z 
2026-01-07T07:06:31.7169224Z HEAD is now at 33f4d35 Merge 1773f4e57f3afede27db430bf0d62315e5e00aff into 9b7421448c99d223f451bd96adab6acbaa6756fd
2026-01-07T07:06:31.7234036Z ##[error]The process 'C:\Program Files\Git\bin\git.exe' failed with exit code 1
2026-01-07T07:06:31.7580177Z Post job cleanup.
2026-01-07T07:06:31.9893865Z [command]"C:\Program Files\Git\bin\git.exe" version
2026-01-07T07:06:32.0238398Z git version 2.52.0.windows.1
2026-01-07T07:06:32.0313232Z Temporarily overriding HOME='D:\a\_temp\47ea592e-7ffb-4765-afda-798d8188ef89' before making global git config changes
2026-01-07T07:06:32.0314284Z Adding repository directory to the temporary git global config as a safe directory
2026-01-07T07:06:32.0325120Z [command]"C:\Program Files\Git\bin\git.exe" config --global --add safe.directory D:\a\requirements-driven-development\requirements-driven-development
2026-01-07T07:06:32.0617958Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp core\.sshCommand
2026-01-07T07:06:32.0902471Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "sh -c \"git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :\""
2026-01-07T07:06:32.6478183Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-01-07T07:06:32.6722439Z http.https://github.com/.extraheader
2026-01-07T07:06:32.6763048Z [command]"C:\Program Files\Git\bin\git.exe" config --local --unset-all http.https://github.com/.extraheader
2026-01-07T07:06:32.7061731Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "sh -c \"git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :\""
2026-01-07T07:06:33.2022170Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-01-07T07:06:33.2304791Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "git config --local --show-origin --name-only --get-regexp remote.origin.url"
2026-01-07T07:06:33.7555848Z Cleaning up orphan processes
