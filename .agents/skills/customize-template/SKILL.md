---
name: customize-template
description: Turn this template repository into a concrete project by renaming the package from `my_project` to a new name and setting the author and description in pyproject.toml, the Sphinx config and the LICENSE. Use right after creating a repository from this template, or whenever the user asks to rename the project, change the package name, or set the author/description.
license: MIT
metadata:
  version: "1.0"
---

# Customize Template

This repository is a template. A new project created from it still carries the
placeholder package name `my_project` and the template author's details. This
skill replaces them consistently across the repository.

## Inputs

Collect these from the user before changing anything. Ask for whatever is
missing; never invent values.

| Input         | Required | Example                     | Notes                                                                                   |
| ------------- | -------- | --------------------------- | --------------------------------------------------------------------------------------- |
| `name`        | yes      | `awesome_lib`               | Lowercase letters, digits, underscores; starts with a letter. Used as the import name. |
| `author`      | yes      | `Jane Doe`                  | Full name.                                                                              |
| `email`       | no       | `jane@example.com`          | Added to `authors` in pyproject.toml when given.                                        |
| `description` | yes      | `An awesome library.`       | One line.                                                                               |

If the user gives a name with hyphens or capitals (e.g. `Awesome-Lib`), suggest
the normalized form (`awesome_lib`) and confirm it.

## What changes

| File                          | Change                                                                                     |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| `src/my_project/`             | Directory renamed to `src/<name>/`.                                                       |
| `src/<name>/__init__.py`      | `__pkg_name__ = "<name>"`.                                                                 |
| `pyproject.toml`              | `name`, `description`, `authors`, and every `src/my_project` / `packages = ["my_project"]` path. |
| `docs/source/conf.py`         | `project`, `author`, and `copyright = "<current year>, <author>"`.                        |
| `docs/source/index.rst`       | Project name in the comment and title (title underline resized).                           |
| `tests/*.py`                  | `import my_project` and references to it.                                                 |
| `LICENSE`                     | `Copyright (c) <current year> <author>`.                                                  |

The script reads the *current* name from `pyproject.toml`, so it also works
when the project has already been renamed once.

## Steps

All commands are single lines so they work the same in bash, zsh, PowerShell
and cmd. `<skill-dir>` is the folder this `SKILL.md` was loaded from, relative
to the repository root: `.agents/skills/customize-template` or
`.claude/skills/customize-template` (the two copies are identical).

1. Make sure you are at the repository root and the working tree is in a state
   the user is happy to modify (mention uncommitted changes if there are any).
2. Preview the changes:

   ```
   uv run --no-project python <skill-dir>/scripts/customize_template.py --name <name> --author "<author>" --email <email> --description "<description>" --dry-run
   ```

   Leave out `--email` if the user did not give one. The script uses only the
   standard library, needs Python 3.11+, and keeps each file's line endings
   (LF or CRLF). Plain `python` instead of `uv run --no-project python` works
   too if a suitable interpreter is on the PATH.
3. Run the same command without `--dry-run`.
4. Refresh the environment and verify:

   ```
   uv lock
   uv sync
   uv run pytest
   ```

5. Search the repository for leftover `my_project` or `my-project` strings,
   skipping `.git`, `.venv` and `uv.lock`, and fix any you find by hand. Use
   your own search tool, or `grep -rn` on Unix and `Select-String` /
   `findstr` on Windows. Do not read or edit the `.env` file.
6. Report to the user what changed, and that the tests pass (or show the
   failure output if they do not).

## Doing it without the script

If the script cannot be run, apply the edits from the "What changes" table by
hand, keeping the existing formatting of each file, then follow steps 4–6.

## Keeping the copies in sync

This skill exists in two identical copies, `.agents/skills/customize-template/`
(for agents that follow the shared `.agents` convention) and
`.claude/skills/customize-template/` (for Claude Code). If you change one, make
the same change in the other.
