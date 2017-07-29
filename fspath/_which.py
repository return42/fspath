# -*- coding: utf-8; mode: python -*-
u"""
which - locate a command
"""
# pylint: disable=invalid-name

import sys
import os
import fspath
from .cli import CLI


# ==============================================================================
def which(cmd, findall=True):
# ==============================================================================
    u"""Searches the fname in the ``PATH`` enviroment.

    This *which* is not POSIX conform.  On Win it searches the ``cmd`` (given
    without extension) in %%PATH%% by adding extensions from %%PATHEXT%%.
    On POSIX it searches for ``cmd`` which is executable.

    If nothing is found, ``None`` is returned. If something matches, a list is
    returned. With option ``findall=False`` the first match is returned or
    ``None``, if nothing is found.

    """
    envpath = os.environ.get('PATH', None) or os.defpath
    hits = list()
    cmd  = fspath.FSPath(cmd)

    if sys.platform == 'win32':
        exe = [x.lower() for x in os.environ.get("PATHEXT", [""]).split(";")]
        for folder in envpath.split(os.pathsep):
            for ext in exe:
                fullname = fspath.FSPath(folder) / cmd + ext
                if fullname.ISFILE:
                    if not findall:
                        return fullname
                    hits.append(fullname)
    else:
        for folder in envpath.split(os.pathsep):
            fullname = fspath.FSPath(folder) / cmd
            if fullname.EXECUTABLE:
                if not findall:
                    return fullname
                hits.append(fullname)
    return hits or None

def _which(cli):
    retVal = 42
    for c in cli.cmd:
        x = which(c, cli.all)
        if x:
            retVal = 0
            if cli.all:
                for hit in x:
                    print(hit)
            else:
                print(x)
    return retVal

_which.__doc__ = which.__doc__

# ==============================================================================
def main():
# ==============================================================================
    u"""
    which command line main function
    """
    cli = CLI(description=__doc__, cmdFunc=_which)

    cli.add_argument(
        "cmd"
        , nargs = "+"
        , type = fspath.FSPath
        , help = "searches CMD in PATH")

    cli.add_argument(
        "-a", "--all", action = 'store_true'
        , help = "print all matching pathnames of each argument" )

    cli()

if __name__ == '__main__':
    sys.exit(main())
