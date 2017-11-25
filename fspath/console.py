# -*- mode: python; coding: utf-8 -*-
# pylint: disable=invalid-name, bad-continuation
"""
Some *console* stuff
"""

import os
import sys

from .helper import Options

CONSOLE_TYPE = None
if (sys.platform.startswith('linux')
    or sys.platform.startswith('darwin')
    or sys.platform.startswith('freebsd')):
    CONSOLE_TYPE = 'tty'

elif sys.platform in ('win32', 'cygwin'):
    CONSOLE_TYPE = 'cmd'
# else:
#     raise NotImplementedError(
#         'The platform %s is not supported yet' % sys.platform)

# ==============================================================================
def consoleDimension():
# ==============================================================================
    u"""Returns count of (row, columns) from current console

    .. hint:

       Since Win-CMD adds a newline if the last column is filled with a
       character it is recomended to use one column less.

    """

    # pylint: disable=broad-except
    rows, columns = 25, 80

    if CONSOLE_TYPE == 'cmd':
        try:
            rows, columns = consoleDimensionsWIN()
        except Exception:
            pass
    else:
        try:
            rows, columns = consoleDimensionsLinux()
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

def consoleDimensionsLinux():
    u"""Returns count of (row, columns) from current console"""
    rows, columns = os.popen('stty size', 'r').read().split()
    return rows, columns

def consoleDimensionsWIN():
    u"""Returns count of (row, columns) from current console"""
    # pylint: disable=too-many-locals
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


# pylint: disable-msg=C0103
KEY = Options(
    # common
    LF      = '\x0d'
    , CR    = '\x0a'
    , ENTER = '\x0d'
    , SPACE = '\x20'
    , ESC   = '\x1b'
    , TAB   = '\x09'

    # CTRL
    , CTRL_A = '\x01'
    , CTRL_B = '\x02'
    , CTRL_C = '\x03'
    , CTRL_D = '\x04'
    , CTRL_E = '\x05'
    , CTRL_F = '\x06'
    , CTRL_Z = '\x1a'

    # ALT
    , ALT_A = '\x1b\x61'

    # CTRL + ALT
    , CTRL_ALT_A = '\x1b\x01'

    # cursors
    , UP    = '\x1b\x5b\x41'
    , DOWN  = '\x1b\x5b\x42'
    , LEFT  = '\x1b\x5b\x44'
    , RIGHT = '\x1b\x5b\x43'

    # other
    , F1  = '\x1b\x4f\x50'
    , F2  = '\x1b\x4f\x51'
    , F3  = '\x1b\x4f\x52'
    , F4  = '\x1b\x4f\x53'
    , F5  = '\x1b\x4f\x31\x35\x7e'
    , F6  = '\x1b\x4f\x31\x37\x7e'
    , F7  = '\x1b\x4f\x31\x38\x7e'
    , F8  = '\x1b\x4f\x31\x39\x7e'
    , F9  = '\x1b\x4f\x32\x30\x7e'
    , F10 = '\x1b\x4f\x32\x31\x7e'
    , F11 = '\x1b\x4f\x32\x33\x7e'
    , F12 = '\x1b\x4f\x32\x34\x7e'

    , PAGE_UP   = '\x1b\x5b\x35\x7e'
    , PAGE_DOWN = '\x1b\x5b\x36\x7e'

    , HOME    = '\x1b\x5b\x48'
    , END     = '\x1b\x5b\x46'
    , BACKTAB = '\x1b\x5b\x5a'

    , BACKSPACE = '\x7f'

    , INSERT = '\x1b\x5b\x32\x7e'
    , DELETE = '\x1b\x5b\x33\x7e'
    )


if CONSOLE_TYPE == 'cmd':

    # ALT
    KEY.ALT_A = None

    # CTRL + ALT
    KEY.CTRL_ALT_A = '\x00\x1e'

    # cursors
    KEY.UP    = '\xe0\x49'
    KEY.DOWN  = '\xe0\x50'
    KEY.LEFT  = '\xe0\x4b'
    KEY.RIGHT = '\xe0\x4d'

    # other
    KEY.F1  = '\x00\x3b'
    KEY.F2  = '\x00\x3c'
    KEY.F3  = '\x00\x3d'
    KEY.F4  = '\x00\x3e'
    KEY.F5  = '\x00\x3f'
    KEY.F6  = '\x00\x40'
    KEY.F7  = '\x00\x41'
    KEY.F8  = '\x00\x42'
    KEY.F9  = '\x00\x43'
    KEY.F10 = '\x00\x44'
    KEY.F11 = '\x00\x85'
    KEY.F12 = '\x00\x86'

    KEY.PAGE_UP   = '\xe0\x49'
    KEY.PAGE_DOWN = '\xe0\x51'

    KEY.HOME    = '\xe0\x47'
    KEY.END     = '\xe0\x4f'
    KEY.BACKTAB = None

    KEY.BACKSPACE = '\x08'

    KEY.INSERT = '\xe0\x52'
    KEY.DELETE = '\xe0\x53'
