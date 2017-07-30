# -*- coding: utf-8; mode: python -*-
u"""semantic path names and more

After 10 years juggling with os.path, zipfile & Co. I thought it is time to
bring back more *pythonic* to APIs. It is made with the philosophy that API's
should be intuitive and their defaults should at least cover 80% of what
programmer daily needs.  Started with the semantic file system pathes, it grows
continuous and includes more and more handy stuff for the daily python
scripting.
"""

from . import __pkginfo__

__version__   = __pkginfo__.version
__author__    = __pkginfo__.authors[0]
__license__   = __pkginfo__.license
__copyright__ = __pkginfo__.copyright

# ==============================================================================
# API
# ==============================================================================

from .fspath import FSPath
from .fspath import callEXE
from .fspath import DevNull

from .cli    import CLI
from .os_env import OS_ENV
from ._which import which

from .progressbar import progressbar

