# Template Repository for Python Projects

This is a template repository intended to be a starting point for Python projects. The repository is equipped with the necessary boilerplate for:

- Project management with `uv`, `hatchling` as the build backend
- Boilerplate for a Python project, structured accorging to the *src layout*
- Documentation with `Sphinx`, with separate source and build folders.
- Tests with `pytest`
- A Makefile with the most commonly used commands
- Configuration for Codacy

## Prerequisites

- uv
- Access to a Databricks Workspace
- Databricks CLI

## Getting Started: Customize the Template

A new repository created from this template still uses the placeholder package name `my_project` and the template author's details. Replace them before doing anything else.

The repository ships an agent skill for this, `customize-template`, written in the open [Agent Skills](https://agentskills.io) format. It comes in two identical copies, because agents look for skills in different folders:

- `.agents/skills/customize-template/` for agents that follow the shared `.agents` convention
- `.claude/skills/customize-template/` for Claude Code

Each copy contains:

```text
SKILL.md                         # instructions for the coding agent
scripts/customize_template.py    # the script that makes the changes
```

If you change the skill, change both copies the same way.

### What it changes

| What | Where |
| --- | --- |
| Package name (`my_project` → your name) | the `src/my_project/` folder, `src/<name>/__init__.py`, `pyproject.toml`, `docs/source/conf.py`, `docs/source/index.rst`, `tests/` |
| Description | `pyproject.toml` |
| Author (and optional email) | `pyproject.toml` (`authors`), `docs/source/conf.py` (`author`, `copyright`), `LICENSE` |

The name must be a valid Python import name: lowercase letters, digits and underscores, starting with a letter (e.g. `awesome_lib`).

### Using it with a coding agent

Ask your agent to run the skill. In Claude Code, type `/customize-template`. In any other agent that supports Agent Skills, ask it something like:

> Customize this template: name it `awesome_lib`, author Jane Doe (jane@example.com), description "An awesome library."

The agent asks for anything you left out, previews the changes, applies them, runs `uv lock`, `uv sync` and `uv run pytest`, and checks for any leftover `my_project` references.

### Using it without an agent

Run the script yourself from the repository root. It needs only the standard library and Python 3.11+, and the commands below work the same in bash, zsh, PowerShell and cmd.

Preview the changes first:

```text
uv run --no-project python .agents/skills/customize-template/scripts/customize_template.py --name awesome_lib --author "Jane Doe" --email jane@example.com --description "An awesome library." --dry-run
```

Then run the same command without `--dry-run`, and refresh and test the project:

```text
uv lock
uv sync
uv run pytest
```

`--email` is optional. Each file keeps its line endings (LF or CRLF). The script reads the current name from `pyproject.toml`, so you can run it again later to rename the project a second time.
