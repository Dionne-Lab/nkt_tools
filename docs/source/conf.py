import sys
import os
import tomli
with open("../../pyproject.toml", "rb") as f:
    toml = tomli.load(f)

sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = toml['project']["name"]
version = toml['project']["version"]
release = toml['project']["version"]
author = ', '.join([entry['name'] for entry in toml['project']["authors"]])

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    "sphinx.ext.intersphinx",
    'sphinx.ext.mathjax'
    ]

autosummary_generate = True
#autodoc_default_options = {'inherited-members': False}

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = []

napoleon_google_docstring = False
napoleon_numpy_docstring = True
todo_include_todos = True

intersphinx_mapping = {
    "python": ("http://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "PyQt5": ("https://www.riverbankcomputing.com/static/Docs/PyQt5/", None)
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_extra_path = ['google98d167b53b925d69.html']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

autodoc_mock_imports = [
    'superk',
    'nkt',
    'ctypes',
    'collections',
    'os'
]
