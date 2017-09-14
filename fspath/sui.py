# -*- mode: python; coding: utf-8 -*-
"""
Simple user interface via terminal (win & *nix)

This module is in a very early stage, don't use it!
"""
# pylint: disable=invalid-name, bad-continuation, wrong-import-position

# ==============================================================================
# imports
# ==============================================================================

import os
import sys
import re

CONSOLE_TYPE = None

if (sys.platform.startswith('linux')
    or sys.platform.startswith('darwin')
    or sys.platform.startswith('freebsd')):
    import tty     # pylint: disable=E0401
    import termios # pylint: disable=E0401
    CONSOLE_TYPE = 'tty'

elif sys.platform in ('win32', 'cygwin'):
    import msvcrt   # pylint: disable=E0401
    CONSOLE_TYPE = 'cmd'
else:
    raise NotImplementedError(
        'The platform %s is not supported yet' % sys.platform)


# ==============================================================================
def consoleDimension():
# ==============================================================================
    u"""Returns count of (row, columns) from current console"""

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

# ==============================================================================
class SimpleUserInterface(object):
# ==============================================================================

    """Simple console based user interface (win & *nix)"""

    ui_out = sys.stdout
    ui_in  = sys.stdin

    if CONSOLE_TYPE == 'tty':
        @classmethod
        def getchr(cls):
            "Get a single unicode character on Linux & Unix."
            f = cls.ui_in.fileno()
            m = termios.tcgetattr(f)
            try:
                tty.setraw(f)
                #ch = codecs.getreader(cls.ui_in.encoding)(cls.ui_in).read(1)
                ch = cls.ui_in.read(1)
            finally:
                termios.tcsetattr(f, termios.TCSADRAIN, m)
            return ch

    elif CONSOLE_TYPE == 'cmd':
        @classmethod
        def getchr(cls):
            "Get a single unicode character on Windows."
            while msvcrt.kbhit():
                # clear keyboard buffer
                msvcrt.getwch()
            ch = msvcrt.getwch()
            if ch in u'\x00\xe0':
                # arrow or function key pressed
                ch = msvcrt.getwch()
            return ch


    @classmethod
    def get_input(cls, count=None, echo=True, valid_chars=r'.', stop_char=u'\r'):
        u"""read input from UI"""
        ret_val = u""
        c = 0
        while count is None or count > c:
            is_valid = False
            while not is_valid:
                ch = cls.getchr()
                if ch == u'\r' or valid_chars is None:
                    is_valid = True
                else:
                    is_valid = bool(re.compile(valid_chars).match(ch))
            c += 1
            if ch == stop_char:
                break
            ret_val += ch
            if echo:
                cls.write(ch)
        return ret_val

    @classmethod
    def write(cls, msg):
        u"""write to UI"""
        #cls.ui_out.write(msg.decode(cls.ui_out.encoding))
        cls.ui_out.write(msg)
        cls.ui_out.flush()

    @classmethod
    def echo(cls, msg):
        u"""write line to UI"""
        cls.write(msg + '\n')

    @classmethod
    def ask_choice(cls, msg, choices, default=0):
        u"""Take a choice from a list via UI"""

        for i in enumerate(choices, 1):
            cls.echo(u"%2d. %s" % i)
        i = None
        while i is None:
            cls.write("%s [%s] " % (msg, default+1))
            c = len(choices)
            u = cls.get_input(count=len(str(c)), valid_chars=r'\d')
            if u == u'':
                i = default
            try:
                i = int(u) - 1
                if i < 0 or i > c:
                    i = None
            except ValueError:
                pass
        return choices[i]

    @classmethod
    def ask(cls, msg, default=None, count=None, echo=True, valid_chars=r'.', stop_char='\r'):
        u"""Ask via UI"""
        cls.write("%s " % msg)
        if default is not None:
            cls.write("[%s] " % default)
        answer = cls.get_input(count=count, echo=echo, valid_chars=valid_chars,
                               stop_char=stop_char)
        if not answer:
            answer = default
        return answer

    YES = 'y'
    NO  = 'n'

    @classmethod
    def ask_yes_no(cls, msg, default='y'):
        u"""Ask Yes/No [YN] via UI"""
        if default not in 'yn':
            raise ValueError('unknown value for default, use "n" or "y"')
        cls.write('%s %s ' % (msg, {'y':'[Y/n]', 'n':'[y/N]'}[default]))
        answer = cls.get_input(count=1, echo=True,  valid_chars=r'[YNyn]')
        if not answer:
            answer = default
        else:
            answer = answer.lower()
        return {'y' : cls.YES, 'n' : cls.NO}[answer]

SUI = SimpleUserInterface()
