# -*- coding: utf-8; mode: python -*-
u"""
A progress bar for the console.
"""
# pylint: disable=invalid-name

import sys

from .console import consoleDimension

# ==============================================================================
def humanizeBytes(size, precision=2):
# ==============================================================================

    """
    Determine the *human readable* value of bytes on 1024 base (1KB=1024B).
    """
    s = ['B ', 'KB', 'MB', 'GB', 'TB']
    x = len(s)
    p = 0
    while size > 1024 and p < x:
        p += 1
        size = size/1024.0
    return "%.*f %s" % (precision, size, s[p])

# ==============================================================================
def progressbar(step, maxSteps, barSize=None, pipe=sys.stdout
                , prompt="", fillchar="=", restchar=" "):
# ==============================================================================

    """
    Show progress-bar

    * step: step number
    * maxSteps: max. steps
    * barSize: char length of the progress-bar
    """

    percent = float(100)/maxSteps*step

    prompt = "\r" + prompt
    if barSize is None:
        barSize = consoleDimension()[1]
        barSize = barSize - 3 - len(prompt) - len(" %3d%%"  % (100,))

    p_bar = fillchar * int(round(percent / 100 * barSize))
    pipe.write((prompt +  "[%s] %3.0f%%") % (p_bar.ljust(barSize, restchar), percent))
    pipe.flush()

