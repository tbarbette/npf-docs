# Configuration file for the Sphinx documentation builder.

# -- Project information

import sys, os


project = 'NPF'
copyright = '2021, Tom Barbette'
author = 'Barbette'

release = '1.0'
version = '1.0.27'

sys.path.append(os.path.abspath('../../../npf'))

autosectionlabel_prefix_document = True

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.intersphinx',
    'sphinx_tabs.tabs',
    'sphinx_toolbox.collapse',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

sphinx_tabs_valid_builders = ['linkcheck']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
