# -*- coding: utf-8; mode: python -*-
u"""fspath: Semantic path names and much more.

After 10 years juggling with os.path, zipfile & Co. I thought it is time to
bring back more *pythonic* to APIs. fspath is made with the philosophy that
API's should be intuitive and their defaults should at least cover 80% of what a
programmer daily needs.  Started with the semantic file system path, it grows
continuous and includes more and more handy stuff for the daily python
scripting."""

__version__     = "20170612"
__copyright__   = "2017 Markus Heiser"
__url__         = "https://github.com/return42/fspath"
__description__ = "Handling path names and executables more comfortable."
__license__     = "GPLv2"

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

