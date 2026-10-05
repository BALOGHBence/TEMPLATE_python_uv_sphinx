# Template Repository for Python Projects

This is a template repository intended to be a starting point for Python projects. The repository is equipped with the necessary boilerplate for:

- Project management with `uv`, `hatchling` as the build backend
- Boilerplate for a Python project, structured accorging to the *src layout*
- Documentation with `Sphinx`, with separate source and build folders.
- Tests with `pytest`
- A Makefile with the most commonly used commands
- Configuration for Codacy

## Prerequisites

- uv (see [Getting Started with uv](#getting-started-with-uv))

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

## Getting Started with uv

[uv](https://docs.astral.sh/uv/) is a fast Python package and project manager from Astral. In this repository it replaces `pip`, `venv`, `pip-tools` and `pyenv`: it installs the right Python version, creates the virtual environment in `.venv/`, resolves dependencies into `uv.lock` and runs commands inside the environment.

### Installing uv

macOS and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

uv is also available through package managers, e.g. `brew install uv`, `winget install --id=astral-sh.uv -e` or `pipx install uv`. Check the installation with `uv --version`. If you used the standalone installer, update uv later with `uv self update`.

You don't need to install Python separately: uv reads the version from `.python-version` (3.12) and downloads it if it isn't on your machine.

### Setting up the project

From the repository root, run:

```bash
uv sync
```

This creates `.venv/`, installs the package in editable mode and installs all dependencies pinned in `uv.lock`. By default uv also installs the `dev` dependency group, which here includes the `test` and `docs` groups. Use `uv sync --no-dev` to install only the runtime dependencies.

### Adding and removing dependencies

Dependencies live in `pyproject.toml`; never edit `uv.lock` by hand. `uv add` and `uv remove` update both files and the environment in one step.

| Goal | Command |
| --- | --- |
| Add a runtime dependency (`[project.dependencies]`) | `uv add requests` |
| Add with a version constraint | `uv add "pandas>=2.2"` |
| Add a development-only tool (`dev` group) | `uv add --dev pre-commit` |
| Add to a specific group (`test`, `docs`, ...) | `uv add --group docs myst-parser` |
| Remove a dependency | `uv remove requests` (add `--dev` or `--group <name>` if it's in a group) |
| Upgrade one package in the lock file | `uv lock --upgrade-package requests` |
| Upgrade everything in the lock file | `uv lock --upgrade` |

Commit both `pyproject.toml` and `uv.lock` so everyone gets the same versions.

### Most important commands

| Command | What it does |
| --- | --- |
| `uv sync` | Make `.venv/` match `uv.lock` exactly (installs missing, removes extra packages) |
| `uv run <command>` | Run a command in the project environment, syncing it first, e.g. `uv run pytest`, `uv run python script.py` |
| `uv add` / `uv remove` | Change dependencies (see above) |
| `uv lock` | Re-resolve dependencies and update `uv.lock` without installing |
| `uv tree` | Show the dependency tree |
| `uv export` | Export the locked dependencies to `requirements.txt` format (see the `Makefile`) |
| `uv python install 3.13` | Install another Python version |
| `uv python pin 3.13` | Change the project's Python version in `.python-version` |
| `uv build` | Build the sdist and wheel into `dist/` |
| `uvx <tool>` | Run a tool in a temporary environment without adding it to the project, e.g. `uvx ruff check` |

With `uv run` you don't need to activate the virtual environment. If you prefer to, activate it with `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows).

Commands you'll use day to day in this repository:

```bash
uv run pytest              # run the tests
uv run ruff check .        # lint
uv run ruff format .       # format
uv run mypy                # type-check
```

### Further reading

- [uv documentation](https://docs.astral.sh/uv/)
- [Installation options](https://docs.astral.sh/uv/getting-started/installation/)
- [Working on projects](https://docs.astral.sh/uv/guides/projects/)
- [Managing dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [Command reference](https://docs.astral.sh/uv/reference/cli/)
- [uv on GitHub](https://github.com/astral-sh/uv)

## Documentation with Sphinx

[Sphinx](https://www.sphinx-doc.org/) builds the project documentation from source files into HTML (and other formats such as PDF or ePub). It is the standard documentation tool in the Python ecosystem: you write pages, link them together with a table of contents (`toctree`), and Sphinx produces a navigable, searchable website.

### Folder layout

The documentation uses separate source and build folders:

```text
docs/
├── Makefile         # build commands for macOS/Linux
├── make.bat         # build commands for Windows
├── source/          # everything you edit
│   ├── conf.py      # Sphinx configuration
│   └── index.rst    # the start page and root table of contents
└── build/           # generated output (ignored by git)
```

Every page you add must be listed in a `toctree`, starting from `index.rst`, or Sphinx warns that it isn't included in any table of contents.

### Writing pages: reStructuredText, MyST Markdown and Jupyter notebooks

You can write pages in three formats and mix them freely:

| Format | File type | Handled by |
| --- | --- | --- |
| reStructuredText | `.rst` | Sphinx itself |
| MyST Markdown | `.md` | [`myst-parser`](https://myst-parser.readthedocs.io/) |
| Jupyter notebooks | `.ipynb` | [`nbsphinx`](https://nbsphinx.readthedocs.io/) |

[MyST](https://mystmd.org/) ("Markedly Structured Text") is a flavour of Markdown that supports everything reStructuredText can do, such as directives, roles and cross-references, so you don't need to learn reStructuredText to write the docs. For example, a note box looks like this in MyST:

````markdown
```{note}
This is a note.
```
````

Notebooks are added to a `toctree` like any other page (by file name, without the extension). Their Markdown cells, code and outputs are rendered as a documentation page, so a notebook can serve as a tutorial or a worked example.

### Building the docs

The `docs` dependency group contains Sphinx and its extensions; `uv sync` installs it as part of the `dev` group. Build the HTML site with:

```bash
uv run make build-docs-html    # macOS/Linux, via the root Makefile
uv run sphinx-build -M html docs/source docs/build    # any platform
```

Open `docs/build/html/index.html` in a browser to view the result. Prefix the command with `uv run` so that `sphinx-build` comes from the project environment.

`nbsphinx` uses [Pandoc](https://pandoc.org/) to convert the Markdown cells of notebooks. The `pandoc` package in the `docs` group is only a Python wrapper, so install the Pandoc program itself as well, e.g. `brew install pandoc` on macOS, `sudo apt install pandoc` on Debian/Ubuntu or `winget install --id JohnMacFarlane.Pandoc` on Windows.

### Configuration in this repository

The configuration lives in `docs/source/conf.py`:

| Setting | Value | Effect |
| --- | --- | --- |
| `extensions` | `myst_parser`, `nbsphinx`, `sphinx_copybutton` | Enables MyST Markdown pages, Jupyter notebook pages and copy buttons on code blocks |
| `html_theme` | `sphinx_rtd_theme` | Uses the [Read the Docs theme](https://sphinx-rtd-theme.readthedocs.io/) |
| `exclude_patterns` | `_build`, `.DS_Store`, `**.ipynb_checkpoints` | Skips build output, macOS metadata and Jupyter autosave copies |
| `templates_path` / `html_static_path` | `_templates` / `_static` | Folders for custom HTML templates and static files (CSS, images) |
| `myst_enable_extensions` | `colon_fence`, `deflist`, `dollarmath` | Allows `:::` fences for directives, definition lists and `$...$` / `$$...$$` math in Markdown |
| `nbsphinx_execute` | `'never'` | Notebooks are **not** run during the build; the outputs saved in the `.ipynb` file are shown. Run and save your notebooks before building |
| `nbsphinx_allow_errors` | `True` | Cells with errors don't stop the build (relevant only if execution is turned on) |
| `copybutton_prompt_text` / `copybutton_prompt_is_regexp` | regex for `>>> `, `... `, `$ `, `In [n]: ` | The copy button strips these prompts, so copied code can be pasted straight into a terminal or interpreter |
| `copybutton_only_copy_prompt_lines` | `False` | Lines without a prompt are copied too |

The project name, author and copyright at the top of `conf.py` are set by the `customize-template` skill (see [Getting Started: Customize the Template](#getting-started-customize-the-template)).

### Further reading

- [Sphinx documentation](https://www.sphinx-doc.org/)
- [Sphinx getting started tutorial](https://www.sphinx-doc.org/en/master/usage/quickstart.html)
- [MyST syntax guide](https://myst-parser.readthedocs.io/en/latest/syntax/typography.html)
- [nbsphinx documentation](https://nbsphinx.readthedocs.io/)
- [sphinx-copybutton documentation](https://sphinx-copybutton.readthedocs.io/)
