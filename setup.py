#!/usr/bin/env python
# -*- coding: utf-8; mode: python -*-

from setuptools import setup, find_packages

__version__     = "20170612"
__copyright__   = "2017 Markus Heiser"
__url__         = "https://github.com/return42/fspath"
__description__ = "Handling path names and executables more comfortable."
__license__     = "GPLv2"

__doc__ = """
The fspath lib simplifies the handling of pathnames and executables. In the
fspath lib, path names are objects with handy methods. If you are a python
developer and tired in juggling with strings of path names and typing all the
time ``os.path.join...`` then you are right here.

:copyright:  Copyright (C) 2017 Markus Heiser
:e-mail:     markus.heiser@darmarIT.de
:license:    GPL Version 2, June 1991 see Linux/COPYING for details.
:docs:       http://return42.github.io/fspath
:repository: `github return42/fspath <https://github.com/return42/fspath>`_

"""

install_requires = [
    "six" ]

setup(
    name               = "fspath"
    , version          = __version__
    , description      = __description__
    , long_description = __doc__
    , url              = __url__
    , author           = "Markus Heiser"
    , author_email     = "markus.heiser@darmarIT.de"
    , license          = __license__
    , keywords         = "path-names development"
    , packages         = find_packages(exclude=['docs', 'tests'])
    , install_requires = install_requires

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
