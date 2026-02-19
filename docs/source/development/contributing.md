# Contributing

## Development Setup

```bash
git clone https://github.com/faulander/pyjira.git
cd pyjira
uv sync --all-extras
```

## Run Tests

```bash
uv run pytest           # run all tests
uv run pytest -v        # verbose output
uv run pytest -x        # stop on first failure
uv run pytest -k search # run only search tests
```

Tests use [respx](https://lundberg.github.io/respx/) to mock httpx requests. No real Jira instance is needed.

## Build Documentation

```bash
uv pip install -r docs/requirements.txt
sphinx-build -b html docs/source docs/build/html
```

Open `docs/build/html/index.html` to preview.

## Project Structure

```
src/pyjira/
    __init__.py          # Public API exports
    client.py            # JiraClient, AsyncJiraClient
    auth.py              # httpx.BasicAuth wrapper
    config.py            # JiraConfig dataclass
    exceptions.py        # Exception hierarchy + raise_for_response()
    pagination.py        # Paginator, AsyncPaginator
    models/              # Pydantic v2 models (23 files)
    resources/           # API resource classes (23 files, sync + async)
tests/                   # Test suite
docs/                    # Sphinx documentation
```

## Conventions

- 2-space indentation
- Single quotes for strings
- `from __future__ import annotations` in every file
- `TYPE_CHECKING` guard for httpx imports
- All model fields are optional (`| None = None`)
- camelCase JSON aliases via `Field(alias='...')`
- Every HTTP call followed by `raise_for_response(response)`
- Dual sync/async pattern: every resource has `FooResource` and `AsyncFooResource`

## Adding a New Resource

1. Create a model file in `src/pyjira/models/` with Pydantic v2 models
2. Create a resource file in `src/pyjira/resources/` with sync + async classes
3. Export models from `src/pyjira/models/__init__.py`
4. Export resources from `src/pyjira/resources/__init__.py`
5. Wire the resource into `JiraClient` and `AsyncJiraClient` in `src/pyjira/client.py`
6. Add public exports to `src/pyjira/__init__.py`
7. Write tests in `tests/`
