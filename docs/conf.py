# -*- coding: utf-8 -*-
#
# Sphinx documentation build configuration file

import os, sys
import fspath

from pallets_sphinx_themes import ProjectLink

sys.path.append(os.path.abspath('../utils/site-python'))
# from sphinx_build_tools import load_sphinx_config

project   = 'FSPath'
copyright = fspath.__copyright__
version   = fspath.__version__
release   = fspath.__version__
show_authors = True

source_suffix       = '.rst'
show_authors        = True
master_doc          = 'index'
templates_path      = ['_templates']
exclude_patterns    = ['_build', 'slides']
todo_include_todos  = True
highlight_language = 'none'

extensions = [
    'sphinx.ext.autodoc'
    , 'sphinx.ext.extlinks'
    #, 'sphinx.ext.autosummary'
    #, 'sphinx.ext.doctest'
    , 'sphinx.ext.todo'
    , 'sphinx.ext.coverage'
    #, 'sphinx.ext.pngmath'
    #, 'sphinx.ext.mathjax'
    , 'sphinx.ext.viewcode'
    , 'sphinx.ext.intersphinx'
    , 'pallets_sphinx_themes'
]

sys.path.append(os.path.abspath('_themes'))
html_theme           = "custom"
html_logo            = 'darmarIT_logo_128.png'
html_theme_path      = ['_themes']
intersphinx_mapping = {}
