# Contributing

## Development setup

1. Install Python 3.14.5 on Windows.
2. Create a virtual environment with `python -m venv .venv`.
3. Activate it and install `python -m pip install -r requirements-dev.txt`.
4. Run the application with `python -m app` or `run.bat`.

## Checks

Run `python -m pytest -q`, `ruff check .`, and `mypy app` before opening a pull request. Keep changes focused, preserve Unicode text, and add a regression test for bug fixes.

## Pull requests

Use a feature branch, describe the user impact, document security and accessibility effects, update the changelog when appropriate, and include exact validation commands. Maintainers review correctness, safety boundaries, performance, and translation completeness before merging.
