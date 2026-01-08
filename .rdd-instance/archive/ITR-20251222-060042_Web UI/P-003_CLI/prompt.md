Implement the CLI backbone (TR-0901, UR-0914)
- Implement rdd.py as the main command router (domain-based):
  - Domains: `prompt`, `workdir`.
  - Interactive menus with curses + numeric fallback (UR-0932).
- Provide wrappers that always use `python` and remain cross-platform (TR-0902).

Acceptance: `python rdd.py --help` works; core actions callable via CLI; errors show cause + remediation (UR-0927).

Docstring should be added to every python function