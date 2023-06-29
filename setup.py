#!/usr/bin/env python
# pylint: disable=C

import os
import io
from setuptools import setup, find_packages

_dir = os.path.abspath(os.path.dirname(__file__))

SRC    = os.path.join(_dir, 'fspath')
README = os.path.join(_dir, 'README.rst')
DOCS   = os.path.join(_dir, 'docs')
TESTS  = os.path.join(_dir, 'tests')

try:
    # Python 2.7
    from imp import load_source
except ImportError:
    import importlib
    def load_source(modname, modpath):
        # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        spec = importlib.util.spec_from_file_location(modname, modpath)
        if not spec:
            raise ValueError("Error loading '%s' module" % modpath)
        module = importlib.util.module_from_spec(spec)
        if not spec.loader:
            raise ValueError("Error loading '%s' module" % modpath)
        spec.loader.exec_module(module)
        return module

# import pkginfo without importing 'fspath/__init__.py' which imports
# third-party dependencies that need to be installed first (e.g. 'six').

PKG = load_source('__pkginfo__', os.path.join(SRC, '__pkginfo__.py'))


def readFile(fname, m='rt', enc='utf-8', nl=None):
    with io.open(fname, mode=m, encoding=enc, newline=nl) as f:
        return f.read()

setup(
    name               = PKG.package
    , version          = PKG.version
    , description      = PKG.description
    , long_description = readFile(README)
    , url              = PKG.url
    , author           = PKG.authors[0]
    , author_email     = PKG.emails[0]
    , license          = PKG.license
    , keywords         = PKG.keywords
    , packages         = find_packages(exclude=['docs', 'tests'])
    , install_requires = PKG.install_requires
    , entry_points     = PKG.get_entry_points()
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    , classifiers      = PKG.classifiers
)
