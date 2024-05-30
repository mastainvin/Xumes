# conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('.'))


# -- Project information

project = 'Xumes'
copyright = '2024, Vincent Mastain'
author = 'Vincent Mastain'
release = '0.1.0'

# -- General configuration



extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_book_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# Ajouter le logo
html_logo = "_static/logo.png"

html_static_path = ['_static']


def setup(app):
    app.add_css_file('custom.css')
