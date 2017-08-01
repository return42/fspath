#!/usr/bin/env python
# -*- coding: utf-8; mode: python -*-
# pylint: disable=invalid-name

u"""
A command line interface made simple.
"""

# ==============================================================================
# imports
# ==============================================================================

import os
import textwrap
import sys
import argparse
import inspect
import code
import linecache

from . import compat
from .os_env import OS_ENV

VERBOSE = False
DEBUG   = bool(OS_ENV.get("DEBUG", False))
QUIET   = False


class HelpFormatter(argparse.HelpFormatter):
    """
    Help message formatter which adds default values to argument help.

    Any formatting in description retains.
    """
    # pylint: disable=redefined-builtin

    def _fill_text(self, text, width, indent):

        text.expandtabs()
        lines = text.splitlines()

        # doc-strings often have no indentation in the first line.

        first = lines[0]
        if first.strip():
            if len(first) - len(first.lstrip(' ')) == 0:
                lines[0] = '    ' + first

        text = textwrap.dedent("\n".join(lines))
        text = compat.indent(text, indent)
        #text = textwrap.fill(text, width = width)
        return text

    def _get_help_string(self, action):
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help += ' (default: %(default)s)'
        return help

class CLIApplError(Exception):
    """Exception raised for errors in the application"""
    # pylint: disable=super-init-not-called
    def __init__(self, exitCode, message):
        self.exitCode = exitCode
        self.message = message

# ==============================================================================
class CLI(object):
# ==============================================================================

    u"""A comfortable command line."""

    OUT = sys.__stdout__
    ERR = sys.__stderr__

    def __init__(self, *args, **kwargs):

        kwargs["formatter_class"] = HelpFormatter

        self.cmdFunc       = kwargs.pop("cmdFunc", None)
        self.cliSubParsers = None

        if self.cmdFunc is not None:
            kwargs["epilog"] = kwargs.get("epilog", self.cmdFunc.__doc__)
            kwargs["description"] = kwargs.get(
                "description"
                , kwargs["epilog"].strip().split("\n")[0] if kwargs["epilog"] else None)

        self.parser = argparse.ArgumentParser(*args, **kwargs)

        if self.cmdFunc is None:
            self.cliSubParsers = self.parser.add_subparsers(title='commands', dest='command')
            self.cliSubParsers.required = True

        self.add_argument  = self.parser.add_argument
        self.add_argument(
            '--debug'
            , action  = 'store_true'
            , help    = 'run in debug mode' )

        self.add_argument(
            '--verbose'
            , action  = 'store_true'
            , help    = 'run in verbose mode' )

        self.add_argument(
            '--quiet'
            , action  = 'store_true'
            , help    = 'run in quiet mode' )

    def addCMDParser(self, func, cmdName=None):
        """Add subcommand parser"""

        if self.cliSubParsers is None:
            raise Exception("this command-line has no sub-commands!")

        subCmd = self.cliSubParsers.add_parser(
            cmdName or func.__name__
            , epilog          = func.__doc__
            , formatter_class = HelpFormatter
            , help            = ((func.__doc__ or "").strip().split("\n") + [ "sorry, no help available" ])[0]
        )
        subCmd.set_defaults(func=func)
        return subCmd

    def __call__(self):

        _exitCode  = 0
        _exception = None
        _retVal    = None

        self.autocomplete()

        cmd_args = self.parser.parse_args()
        cmd_args.CLI = self
        cmd_args.OUT = self.OUT
        cmd_args.ERR = self.ERR
        cmd_args.Error = CLIApplError

        if OS_ENV.get("DEBUG", None):
            cmd_args.debug = True

        # pylint: disable=W0603
        global DEBUG, VERBOSE, QUIET
        DEBUG   = cmd_args.debug
        VERBOSE = cmd_args.verbose
        QUIET   = cmd_args.quiet

        if DEBUG:
            self.OUT.write(u"argparse --> %s\n" % cmd_args)
            __builtins__["CONSOLE"] = CONSOLE

        try:
            if self.cmdFunc is None:
                _retVal = cmd_args.func(cmd_args)
            else:
                _retVal = self.cmdFunc(cmd_args)
            try:
                if _retVal is None:
                    _exitCode = 0
                else:
                    _exitCode = int(_retVal)
            except Exception as exc: # pylint: disable=W0703
                pass

        except CLIApplError as exc: # pylint: disable=W0703
            _exitCode  = exc.exitCode
            self.ERR.write(u"ERROR (%s): %s\n" % (exc.exitCode, exc.message))

        except Exception as exc: # pylint: disable=W0703
            if cmd_args.debug:
                raise
            _exitCode  = 42
            _exception = str(exc)
            sys.stderr.write(u"FATAL ERROR: %s\n" % _exception)
        sys.exit(_exitCode)

    def autocomplete(self):
        u"""bash completion

        To get in use of bash completion, install ``argcomplete``:

        .. code-block:: bash

           pip install argcomplete

        and add the following to your ~/.bashrc:

        .. code-block:: bash

           function _py_argcomplete() {
                   local IFS=$(echo -e '\\v')
                   COMPREPLY=( $(IFS="$IFS" \\
                           COMP_LINE="$COMP_LINE" \\
                           COMP_POINT="$COMP_POINT" \\
                           _ARGCOMPLETE_COMP_WORDBREAKS="$COMP_WORDBREAKS" \\
                           _ARGCOMPLETE=1 \\
                           "$1" 8>&1 9>&2 1>/dev/null) )
                   if [[ $? != 0 ]]; then
                           unset COMPREPLY
                   fi
           }
           complete -o nospace -o default -F _py_argcomplete myCommandName

        ..
        """

        # only complete when called from _py_argcomplete()
        if '_ARGCOMPLETE' not in os.environ:
            return
        try:
            import argcomplete  # pylint: disable=import-error
        except ImportError:
            self.ERR.write("TAB-completion, python-argcomplete not installed.")
            sys.exit(1)
        argcomplete.autocomplete(self.parser)


def CONSOLE(arround=5, frame=None):
    u"""
    2cent debugging & introspection
    """
    # pylint: disable=C0321,C0410

    sys.stderr.flush()
    sys.stdout.flush()

    frame  = frame or inspect.currentframe().f_back
    fName  = frame.f_code.co_filename
    lineNo = frame.f_lineno

    ns = dict(**frame.f_globals)
    ns.update(**frame.f_locals)

    histfile = os.path.join(os.path.expanduser("~"), ".kernel-doc-history")
    try:
        import readline, rlcompleter  # pylint: disable=W0612
        readline.set_completer(rlcompleter.Completer(namespace=ns).complete)
        readline.parse_and_bind("tab: complete")
        readline.set_history_length(1000)
        if os.path.exists(histfile):
            readline.read_history_file(histfile)
    except ImportError:
        readline = None
    lines  = []
    for c in range(lineNo - arround, lineNo + arround):
        if c > 0:
            prefix = "%-04s|" % c
            if c == lineNo:   prefix = "---->"
            line = linecache.getline(fName, c, frame.f_globals)
            if line != '':    lines.append(prefix + line)
            else:
                if lines: lines[-1] = lines[-1] + "<EOF>\n"
                break
    banner =  "".join(lines) + "file: %s:%s\n" % (fName, lineNo)
    try:
        code.interact(banner=banner, local=ns)
    finally:
        if readline is not None:
            readline.write_history_file(histfile)

def DUMMY_CONSOLE(*_x, **_y):
    u"""A dummy console, spid out warnings for usage of 'CONSOLE' without activated DEBUG
    environment.
    """
    frame  = inspect.currentframe().f_back
    fName  = frame.f_code.co_filename
    lineNo = frame.f_lineno
    sys.stderr.write("%s:%s: [WARNING] usage of CONSOLE / debug not activated!\n" % (fName, lineNo))

__builtins__["CONSOLE"] = DUMMY_CONSOLE
if DEBUG:
    __builtins__["CONSOLE"] = CONSOLE

