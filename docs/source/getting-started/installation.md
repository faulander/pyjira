# Installation

## Requirements

- Python 3.12 or later
- A Jira Cloud instance with an [API token](https://id.atlassian.com/manage/api-tokens)

## Install from PyPI

Using [uv](https://docs.astral.sh/uv/):

```bash
uv add pyjiraV3
```

Using pip:

```bash
pip install pyjiraV3
```

## Install from Source

```bash
git clone https://github.com/faulander/pyjira.git
cd pyjira
uv sync
```

## Dependencies

pyJiraV3 has minimal runtime dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| [httpx](https://www.python-httpx.org/) | >= 0.28 | HTTP client with sync and async support |
| [pydantic](https://docs.pydantic.dev/) | >= 2.0 | Data validation and typed models |

## Verify Installation

```python
import pyjira
print(pyjira.__version__)
```
