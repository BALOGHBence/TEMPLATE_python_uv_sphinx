# Instructions for Coding Agents

Never ever read the `.env` file in the repository!!!

## Ownership

The commit messages shouldn't include any details on ownership at all.

Never add "Co-Authored-By: Claude..." or similar AI contributor lines to commit messages. Commit messages are not the place to make ownership statements — ownership of code is governed by company policies and agreements between employer and employee, or by the individual repository owner if no organization is involved.

## Code Style

### PEP 8

All Python code must comply with [PEP 8](https://peps.python.org/pep-0008/). Ruff enforces it (configured in `pyproject.toml`), so before finishing a change run:

```bash
uv run ruff format .
uv run ruff check .
```

Fix every reported issue instead of silencing it. Only add a `# noqa` comment when there is a good reason, and state the reason next to it.

### NumPy-style docstrings

Every public module, class, function and method must have a docstring in the [NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html). Do not use Google-style or reStructuredText-style (`:param x:`) docstrings. Include the sections that apply, in this order: a one-line summary, an extended description, `Parameters`, `Returns` (or `Yields`), `Raises` and `Examples`.

```python
def scale(values: list[float], factor: float = 1.0) -> list[float]:
    """Multiply every value by a constant factor.

    Parameters
    ----------
    values : list[float]
        The numbers to scale.
    factor : float, optional
        The multiplier, by default 1.0.

    Returns
    -------
    list[float]
        The scaled values, in the original order.

    Raises
    ------
    ValueError
        If `values` is empty.

    Examples
    --------
    >>> scale([1.0, 2.0], factor=3.0)
    [3.0, 6.0]
    """
```

### Type hints

Add type hints to function signatures and to any variable whose type isn't obvious. mypy runs in strict mode (`uv run mypy`), so code without annotations will fail the check. Use modern syntax for Python 3.12+: built-in generics (`list[str]`, `dict[str, int]`), `X | None` instead of `Optional[X]`, and the `type` statement for type aliases. Avoid `Any` unless there is no better option.
