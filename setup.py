#!/usr/bin/env python
# -*- coding: utf-8; mode: python -*-

from setuptools import setup, find_packages
import fspath

setup(
    name               = "fspath"
    , version          = fspath.__version__
    , description      = fspath.__description__
    , long_description = fspath.__doc__
    , url              = fspath.__url__
    , author           = "Markus Heiser"
    , author_email     = "markus.heiser@darmarIT.de"
    , license          = fspath.__license__
    , keywords         = "path-names development"
    , packages         = find_packages(exclude=['docs', 'tests'])
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    , classifiers = [
        "Development Status :: 5 - Production/Stable"
        , "Intended Audience :: Developers"
        , "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
        , "Operating System :: OS Independent"
        , "Programming Language :: Python"
        , "Programming Language :: Python :: 2"
        , "Programming Language :: Python :: 3"
        , "Topic :: Utilities"
        , "Topic :: Software Development :: Libraries"
        , "Topic :: System :: Filesystems" ]
)
