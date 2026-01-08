```markdown
# Analysis for prompt P-012 — Tests Troubleshoot 2

## Copilot Review

Issue summary: the CI job fails with `ERROR: file or directory not found: tests/python/` when running `pytest tests/python/` in the Linux workflow. This indicates pytest was invoked with a path that does not exist from the current working directory or the tests were not checked out to the expected location.

Assessment:
- Potential risks and challenges: the failure prevents test execution and blocks merges; changing runner commands risks hiding other environment issues if not validated; incorrect relative paths may break both local and CI test runs.
- Impact on existing functionality: CI will fail on pull requests targeting `dev`, blocking automatic validation and releases until fixed.
- Completeness of the prompt description: the prompt provides the failing log and the command used, which is sufficient to form hypotheses but lacks the content of `scripts/run-tests.py` and the CI workflow YAML which determine working directory and invocation context.

## Best Practices

- Prefer invoking tests with the selected interpreter to avoid PATH issues: use `python -m pytest tests/python/` rather than bare `pytest` so the `python` in the virtual environment runs pytest.
- Use repository-root detection for relative paths in scripts: compute `repo_root = Path(__file__).resolve().parents[<n>]` or use `git rev-parse --show-toplevel` to avoid brittle relative paths.
- In CI workflows, explicitly set `working-directory` where needed or use steps to `ls` and debug checkout contents when failures occur.
- Ensure `scripts/setup-test-env.py` echoes the venv activation and prints `pwd` and `ls -la` in CI to help diagnose missing files.

URLs checked (representative):
- https://docs.pytest.org/en/stable/usage.html — pytest invocation recommendations and path handling.
- https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions — `working-directory` and checkout behaviors.
- https://docs.python.org/3/library/__main__.html#module-python - guidance for `python -m` usage.

Summary of findings from references: prefer `python -m pytest` to ensure correct interpreter; CI steps should not rely on implicit current directories; add diagnostic `ls` steps to identify content at runtime.

## Proposals

1) Quick fix (minimal, safe): Update `scripts/run-tests.py` to invoke tests using the project root and the `python -m pytest` form. Example: determine project root via `Path(__file__).resolve().parents[2]` and run `subprocess.run([sys.executable, '-m', 'pytest', str(project_root / 'tests' / 'python')])`.

2) CI robustness: Modify `.github/workflows/tests.yml` to explicitly set `working-directory: ${{ github.workspace }}` or ensure `actions/checkout` step leaves the repository contents at the expected path; add a debug step before running tests to `ls -R` the repo root.

3) Environment guardrails: Ensure `scripts/setup-test-env.py` creates and activates a virtual environment using `python -m venv .venv` and then installs test deps into it; the test runner should call `sys.executable` when invoking pytest to avoid discrepancies between `python` and `python3` executables.

4) Long-term: Enhance `scripts/run-tests.py` to accept a base-path argument and add a `--rdd-framework` flag as specified in the Tests enhancement prompt so CI can call the exact test subset reliably.

Trade-offs:
- Changing the CI workflow is fast and fixes the immediate symptom but may mask deeper path-handling bugs in scripts; updating `run-tests.py` to be root-aware fixes both local and CI runs and is preferable.

## Prompt Modification

Refined prompt text (suggested):

"Linux CI run fails with `ERROR: file or directory not found: tests/python/` when executing the repository's test suite in GitHub Actions. Investigate likely causes (incorrect working directory in CI, brittle relative paths in `scripts/run-tests.py`, or missing test checkout), propose specific code changes to `scripts/run-tests.py` and the CI workflow to reliably run tests on Linux, implement the minimal safe fix that ensures both local and CI test execution succeed, and document the change in `[IMPLEMENTATION]` with rationale. Do not modify other unrelated files."

---

Generated-by: RDD Analyzer

```
