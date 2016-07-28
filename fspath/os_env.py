#!/usr/bin/env python
u"""
Environment access more comfortable.
"""

import os

# ==============================================================================
class OS_ENV(dict):
# ==============================================================================

    u"""
    Environment object (singleton).

    .. code-block:: python

       >>> if OS_ENV.get("SHELL") is None:
               OS_ENV.SHELL = "/bin/bash"
       >>> OS_ENV.MY_NAME
       '/bin/bash'
    """
    @property
    def __dict__(self):
        return os.environ

    def __getattr__(self, attr):
        return os.environ[attr]

    def __setattr__(self, attr, val):
        os.environ[attr] = val

    def get(self, attr, default=None):
        return os.environ.get(attr, default)

OS_ENV = OS_ENV()
