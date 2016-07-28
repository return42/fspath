# -*- coding: utf-8; mode: python -*-
u"""
The fspath lib simplifies the handling of pathnames and executables. In the
fspath lib, path names are objects with handy methods. If you are a python
developer and tired in juggling with strings of path names and typing all the
time ``os.path.join...`` then you are right here.

:copyright:  Copyright (C) 2016 Markus Heiser
:license:    GPL Version 2, June 1991 see Linux/COPYING for details.

"""

from .fspath import FSPath
from .fspath import which
from .fspath import callEXE
from .fspath import DevNull
from .os_env import OS_ENV

from .progressbar import progressbar
from .progressbar import consoleDimension

__version__     = "20160722"
__copyright__   = "2016 Markus Heiser"
__url__         = "https://github.com/return42/fspath"
__description__ = "Handling path names and executables more comfortable."
__license__     = "GPLv2"

