# conf.py
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

# -- Project information

project = 'Xumes'
copyright = '2024, Vincent Mastain'
author = 'Vincent Mastain'
description = 'Xumes is a test automation framework for Games in Game Engines using reinforcement learning.'
release = "0.3.0"
html_title = f'<strong>Xumes {release}</strong>  <small>🤖 ✔️</small>'
html_short_title = description

# -- General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_copybutton',
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

html_theme = 'furo'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# html_logo = "_static/logo.png"
# Options spécifiques à Furo pour les logos
html_static_path = ['_static']

html_theme_options = {
    "light_logo": "logo_lightmode.png",
    "dark_logo": "logo_darkmode.png",
}

from docutils import nodes
from docutils.parsers.rst import directives

IFRAME_CODE = """<iframe width="%(width)s" height="%(height)s"
src="https://www.youtube.com/embed/%(yid)s" frameborder="0"
allowfullscreen>%(extra)s</iframe>
"""


def youtube(name, args, options, content, lineno,
            contentOffset, blockText, state, stateMachine):
    """ Restructured text extension for inserting youtube embedded videos """
    if len(content) == 0:
        return
    string_vars = {
        'yid': content[0],
        'width': '560',  # default width
        'height': '315',  # default height
        'extra': ''
    }
    extra_args = content[1:]  # Because content[0] is ID
    extra_args = [ea.strip().split("=") for ea in extra_args]  # key=value
    extra_args = [ea for ea in extra_args if len(ea) == 2]  # drop bad lines
    extra_args = dict(extra_args)
    if 'width' in extra_args:
        string_vars['width'] = extra_args.pop('width')
    if 'height' in extra_args:
        string_vars['height'] = extra_args.pop('height')
    if extra_args:
        params = ["%s='%s'" % (key, extra_args[key]) for key in extra_args]
        string_vars['extra'] = " ".join(params)
    return [nodes.raw('', IFRAME_CODE % (string_vars), format='html')]


youtube.content = True
directives.register_directive('youtube', youtube)
