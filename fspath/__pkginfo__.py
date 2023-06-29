# -*- coding: utf-8; mode: python -*-
# pylint: disable=invalid-name,redefined-builtin
"""
python package meta informations
"""
import platform

package      = 'fspath'
version      = '20230629'
authors      = ['Markus Heiser', ]
emails       = ['markus.heiser@darmarIT.de', ]
copyright    = '2023 Markus Heiser'
url          = 'https://github.com/return42/fspath'
description  = 'semantic path names and more'
license      = 'AGPLv3'
keywords     = "path-names development"

def get_entry_points():
    """get entry points of the python package"""
    # To not compete with POSIXs 'which', fspaths 'which'
    # will be installed as .py
    _which = 'which.py'
    if platform.system() == 'Windows':
        # on OS M$Win, there is no which preinstalled
        _which = 'which'
    return {
        'console_scripts': [
            _which + ' = fspath._which:main'
            , 'fspath = fspath.main:main'
        ]}

install_requires = [
    "six" ]

classifiers = [
    "Development Status :: 5 - Production/Stable"
    , "Intended Audience :: Developers"
    , "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
    , "Operating System :: OS Independent"
    , "Programming Language :: Python"
    , "Programming Language :: Python :: 2"
    , "Programming Language :: Python :: 3"
    , "Topic :: Utilities"
    , "Topic :: Software Development :: Libraries"
    , "Topic :: System :: Filesystems" ]
