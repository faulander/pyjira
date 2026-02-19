import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "pyJiraV3"
copyright = "2025, faulander"
author = "faulander"
release = "0.1.2"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]
html_title = "pyJiraV3"

autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_class_signature = "separated"
napoleon_google_docstrings = True
napoleon_numpy_docstrings = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "httpx": ("https://www.python-httpx.org/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
