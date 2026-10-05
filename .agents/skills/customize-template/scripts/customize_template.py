"""Customize this template repository: rename the package and set its metadata.

Run from anywhere inside the repository with the Python interpreter of your
choice (standard library only, Python >= 3.11):

    python .agents/skills/customize-template/scripts/customize_template.py \
        --name awesome_lib \
        --author "Jane Doe" \
        --email jane@example.com \
        --description "An awesome library."

The current project name and author are read from the repository itself, so
the script can be run again later to rename the project a second time.
Use ``--dry-run`` to preview the changes without touching any file.
"""

from __future__ import annotations

import argparse
import datetime
import json
import keyword
import re
import sys
import tomllib
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def find_repo_root() -> Path:
    for candidate in [Path.cwd(), *Path.cwd().parents]:
        if (candidate / "pyproject.toml").is_file() and (candidate / "src").is_dir():
            return candidate
    sys.exit("error: could not find the repository root (pyproject.toml + src/)")


def toml_str(value: str) -> str:
    # JSON string escaping is a valid TOML basic string.
    return json.dumps(value, ensure_ascii=False)


def sub_once(pattern: str, repl: str, text: str, what: str) -> str:
    new_text, count = re.subn(pattern, lambda _: repl, text, count=1, flags=re.M)
    if count == 0:
        sys.exit(f"error: could not find {what}")
    return new_text


class Customizer:
    def __init__(self, root: Path, dry_run: bool) -> None:
        self.root = root
        self.dry_run = dry_run

    def edit(self, rel_path: str, transform) -> None:  # type: ignore[no-untyped-def]
        path = self.root / rel_path
        if not path.is_file():
            print(f"skip    {rel_path} (not found)")
            return
        # Keep the file's own line endings (LF or CRLF) on every platform.
        with path.open(encoding="utf-8", newline="") as f:
            raw = f.read()
        newline = "\r\n" if "\r\n" in raw else "\n"
        old = raw.replace("\r\n", "\n")
        new = transform(old)
        if new == old:
            print(f"same    {rel_path}")
            return
        print(f"update  {rel_path}")
        if not self.dry_run:
            with path.open("w", encoding="utf-8", newline="") as f:
                f.write(new.replace("\n", newline))

    def rename_dir(self, old_rel: str, new_rel: str) -> None:
        old_path, new_path = self.root / old_rel, self.root / new_rel
        if old_path == new_path:
            return
        if not old_path.is_dir():
            sys.exit(f"error: package directory {old_rel} does not exist")
        if new_path.exists():
            sys.exit(f"error: {new_rel} already exists")
        print(f"rename  {old_rel} -> {new_rel}")
        if not self.dry_run:
            old_path.rename(new_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--name", required=True, help="new project / import name, e.g. awesome_lib")
    parser.add_argument("--author", required=True, help="author's full name")
    parser.add_argument("--email", default="", help="author's email (optional)")
    parser.add_argument("--description", required=True, help="one-line project description")
    parser.add_argument("--dry-run", action="store_true", help="only print what would change")
    args = parser.parse_args()

    new_name: str = args.name
    if not NAME_PATTERN.match(new_name) or keyword.iskeyword(new_name):
        sys.exit(
            f"error: invalid name {new_name!r}; use lowercase letters, digits and "
            "underscores, starting with a letter (it must be importable in Python)"
        )

    root = find_repo_root()
    pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    old_name: str = pyproject["project"]["name"]
    year = datetime.date.today().year

    author, email, description = args.author, args.email, args.description
    authors_entry = f"{{ name = {toml_str(author)}" + (
        f", email = {toml_str(email)} }}" if email else " }"
    )

    print(f"Customizing {root}")
    print(f"  name:        {old_name} -> {new_name}")
    print(f"  author:      {author}" + (f" <{email}>" if email else ""))
    print(f"  description: {description}")
    if args.dry_run:
        print("  (dry run, nothing will be written)")
    print()

    c = Customizer(root, args.dry_run)
    word = re.compile(rf"\b{re.escape(old_name)}\b")

    def pyproject_toml(text: str) -> str:
        text = sub_once(r'^name = ".*"$', f"name = {toml_str(new_name)}", text, "project name")
        description_line = f"description = {toml_str(description)}"
        authors_line = f"authors = [{authors_entry}]"
        if re.search(r"^authors = .*$", text, flags=re.M):
            text = sub_once(r"^authors = .*$", authors_line, text, "authors")
            text = sub_once(r"^description = .*$", description_line, text, "description")
        else:
            text = sub_once(
                r"^description = .*$",
                f"{description_line}\n{authors_line}",
                text,
                "description",
            )
        text = text.replace(f"src/{old_name}", f"src/{new_name}")
        text = text.replace(f'packages = ["{old_name}"]', f'packages = ["{new_name}"]')
        return text

    def conf_py(text: str) -> str:
        text = sub_once(r"^project = .*$", f"project = {new_name!r}", text, "Sphinx project")
        text = sub_once(r"^author = .*$", f"author = {author!r}", text, "Sphinx author")
        text = sub_once(
            r"^copyright = .*$", f"copyright = {f'{year}, {author}'!r}", text, "Sphinx copyright"
        )
        return text

    def init_py(text: str) -> str:
        return sub_once(
            r"^__pkg_name__ = .*$", f"__pkg_name__ = {toml_str(new_name)}", text, "__pkg_name__"
        )

    def index_rst(text: str) -> str:
        text = word.sub(new_name, text)
        # Keep the title underline as long as the title itself.
        return re.sub(
            r"^(.+ documentation)\n=+$",
            lambda m: f"{m.group(1)}\n{'=' * len(m.group(1))}",
            text,
            count=1,
            flags=re.M,
        )

    def license_txt(text: str) -> str:
        return sub_once(
            r"^Copyright \(c\) .*$", f"Copyright (c) {year} {author}", text, "LICENSE copyright"
        )

    c.edit("pyproject.toml", pyproject_toml)
    c.edit("docs/source/conf.py", conf_py)
    c.edit(f"src/{old_name}/__init__.py", init_py)
    c.edit("docs/source/index.rst", index_rst)
    for test_file in sorted((root / "tests").glob("*.py")):
        c.edit(str(test_file.relative_to(root)), lambda t: word.sub(new_name, t))
    c.edit("LICENSE", license_txt)
    c.rename_dir(f"src/{old_name}", f"src/{new_name}")

    print()
    if args.dry_run:
        print("Dry run finished. Re-run without --dry-run to apply the changes.")
    else:
        print("Done. Next steps:")
        print("  uv lock && uv sync     # refresh the lock file with the new name")
        print("  uv run pytest          # check that the package still imports")


if __name__ == "__main__":
    main()
