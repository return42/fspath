# -*- coding: utf-8; mode: python -*-
u"""
A progress bar for the console.
"""

import os
import sys

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

    p_bar = fillchar * int(percent / 100 * barSize)
    pipe.write((prompt +  "[%s] %3d%%") % (p_bar.ljust(barSize, restchar), int(percent)))
    pipe.flush()

# ==============================================================================
def consoleDimension():
# ==============================================================================
    # pylint: disable=W0703

    rows, columns = 25, 80

    import platform
    if platform.system() == 'Windows':
        try:
            rows, columns = _consoleDimensionsWIN()
        except Exception:
            pass
    else:
        try:
            rows, columns = _consoleDimensionsLinux()
        except Exception:
            pass
    try:
        rows = int(rows)
    except Exception:
        pass

    try:
        columns = int(columns)
    except Exception:
        pass

    return rows, columns

def _consoleDimensionsLinux():
    rows, columns = os.popen('stty size', 'r').read().split()
    return rows, columns

def _consoleDimensionsWIN():

    # pylint: disable=R0914
    from ctypes import windll, create_string_buffer

    # stdin handle is -10
    # stdout handle is -11
    # stderr handle is -12

    h = windll.kernel32.GetStdHandle(-12)
    csbi = create_string_buffer(22)
    res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

    columns, rows = 80, 25
    if res:
        import struct
        (_bufx, _bufy, _curx, _cury, _wattr,
         left, top, right, bottom, _maxx, _maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        columns = right - left + 1
        rows    = bottom - top + 1

    return rows, columns
