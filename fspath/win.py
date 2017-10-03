# -*- coding: utf-8; mode: python -*-
u"""
Windows stuff
"""
# pylint: disable=invalid-name

import os
import io
import six
from .fspath import FSPath

# ==============================================================================
def wrapScriptExe(script, shebang = u"#!python.exe"):
# ==============================================================================
    u"""Wraps a single script into a MS-Win ``.exe``.

    Only the ``script`` file contents is wraped into the ``.exe``, not the whole
    python environment!

    This is usefull to create ``.exe`` console scripts for python entry points,
    which can be called directly (``myscript.exe`` instead ``python
    myscript.py``).

    .. caution::

       * This is in an experimental state!
       * This makes use of undocumented pip APIs (ATM pip has no offical API)
       * Use it with care!
       * Shebang is always ``#!python.exe``

    """

    from pip._vendor.distlib.scripts import ScriptMaker
    from pip._vendor.distlib.compat import ZipFile

    origin   = FSPath(script)
    exec_out = origin.suffix('.exe')
    shebang  = six.b(shebang + u"\r\n")
    linesep  = os.linesep.encode('utf-8')

    script   = origin.readFile()
    script   = six.b(script)

    maker    = ScriptMaker(source_dir    = origin.DIRNAME
                           , target_dir  = origin.DIRNAME)

    if origin.SUFFIX == '.py':
        launcher = maker._get_launcher('t') # pylint: disable=protected-access
    else:
        launcher = maker._get_launcher('w') # pylint: disable=protected-access

    stream = io.BytesIO()
    with ZipFile(stream, 'w') as _f:
        if six.PY2:
            _f.writestr('__main__.py', str(script))
        else:
            _f.writestr('__main__.py', script)

    zip_data = stream.getvalue()
    if six.PY2:
        script = launcher + str(shebang + linesep) + zip_data
    else:
        script = launcher + shebang + linesep + zip_data

    with open(exec_out, "wb") as out:
        out.write(script)

    #print("created %s" % exec_out)
    return exec_out

    # On Windows, we have no exec bit
    #
    # def set_mode(bits, mask, filename):
    #     if os.name == 'posix' or (os.name == 'java' and os._name == 'posix'):
    #         # Set the executable bits (owner, group, and world) on
    #         # all the files specified.
    #         mode = (os.stat(filename).st_mode | bits) & mask
    #         os.chmod(f, mode)
    #
    # set_executable_mode = lambda f: set_mode(0o555, 0o7777, f)
    # set_executable_mode(exec_out)

def _cli_py2exe(cli):
    print("created %s" % wrapScriptExe(cli.script, cli.shebang))

_cli_py2exe.__doc__ = wrapScriptExe.__doc__
