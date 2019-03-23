#!/usr/bin/env python
# -*- coding: utf-8; mode: python -*-
# pylint: disable=invalid-name, logging-not-lazy

"""
Small collection for debugging and introspection purpose.
"""

# ==============================================================================
#  imports ...
# ==============================================================================

import sys
import socket
import pdb
import inspect
import linecache
import time
import logging

from code   import InteractiveConsole
from codeop import CommandCompiler
from telnetlib import Telnet
import six

__all__ = ['Console', 'RemoteConsole', 'RemotePdb', 'rtrace', 'trace']

logger = logging.getLogger('fspath.debug')
ERROR  = logger.error

# ==============================================================================
def descrFrame(frame, arround=3):
# ==============================================================================
    u"""get description of the code frame"""
    fName  = frame.f_code.co_filename
    lineNo = frame.f_lineno
    lines = []
    for c in range(lineNo - arround, lineNo + arround):
        if c > 0:
            prefix = "%-04s|" % c
            if c == lineNo:
                prefix = "---->"
            line = linecache.getline(fName, c, frame.f_globals)
            if line != '':
                lines.append(prefix + line)
            else:
                if lines:
                    lines[-1] = lines[-1] + "<EOF>\n"
                break
    retVal = (
        "".join(lines)
        + "file: %s:%s\n" % (fName, lineNo)
        )
    return retVal

# ==============================================================================
class Console(InteractiveConsole):
# ==============================================================================

    u"""A simple interactive console.
    """

    EOF = None

    # pylint: disable=super-init-not-called
    def __init__(self, local_ns=None, global_ns=None, filename="<console>"):
        if local_ns is None:
            local_ns = {"__name__": "__console__", "__doc__": None}

        if global_ns is None:
            global_ns = {}

        self.local_ns  = local_ns
        self.global_ns = global_ns
        self.compile   = CommandCompiler()
        self.filename = filename
        self.resetbuffer()

    def raw_input(self, prompt=""):
        if self.EOF is None:
            return six.moves.input(prompt)
        sys.stdout.write(prompt)
        sys.stdout.flush()
        line = sys.stdin.readline()
        ERROR(repr(line))
        if line.strip() == self.EOF:
            raise EOFError
        return line

    def write(self, data):
        sys.stdout.write(data)
        sys.stdout.flush()

    def runcode(self, code):
        try:
            exec(code, self.global_ns, self.local_ns) # pylint: disable=W0122
        except SystemExit:   # pylint: disable=try-except-raise
            raise
        except Exception:    # pylint: disable=W0703
            self.showtraceback()

    @classmethod
    def run(cls, local_ns=None, global_ns=None
            , banner=None, filename="<console>"
            , frame=None, EOF=None): # pylint: disable=C0103
        u"""Start console

        Without setting explicit namespaces (``local_ns``, ``global_ns``),
        the namespaces from the current code-frame are uused.

        .. code-block:: python

          def foo(arg1):
              ...
              Console.run()

        """
        frame = frame or inspect.currentframe().f_back
        if banner is None:
            banner = "console ...\n%s" % descrFrame(frame)
        if local_ns is None:
            local_ns = frame.f_locals
        if global_ns is None:
            global_ns = frame.f_globals
        #inspect.currentframe().f_back
        console = cls(local_ns, global_ns, filename)
        if EOF:
            banner += "\nExit console with %r" % EOF
            console.EOF = EOF # pylint: disable=C0103
        console.interact(banner=banner)

# ==============================================================================
class RemoteConsole(Console):
# ==============================================================================

    u"""A simple remote console.

    Works just like the ``Console`` except the console can be reached from a
    remote (terminal session).
    """

    EOF = 'EOF'

    def interact(self, port, addr="127.0.0.1", banner=None): # pylint: disable=arguments-differ

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        old_stdin  = sys.stdin

        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        skt.bind((addr, port))
        skt.listen(1)
        ERROR("accept connection %s:%s" % (addr, port))
        (conn, remote) = skt.accept()
        ERROR("got connection from %s:%s" % remote)
        rwStream = conn.makefile('rw', 0)
        ERROR("redirect")
        sys.stderr = sys.stdout = sys.stdin = rwStream

        try:
            Console.interact(self, banner)
        except Exception as exc:  # pylint: disable=W0703
            ERROR(str(exc))

        try:
            rwStream.close()
        except Exception as exc:  # pylint: disable=W0703
            ERROR("error on closing stream: " + str(exc))

        try:
            skt.close()
        except Exception as exc:  # pylint: disable=W0703
            ERROR("error on closing socket: " + str(exc))

        #ERROR("re-redirect")
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        sys.stdin  = old_stdin
        ERROR("close connection ...")
        ERROR("connection %s:%s closed" % remote)

    @classmethod
    def run(cls, port, local_ns=None, global_ns=None  # pylint: disable=arguments-differ
            , banner=None, filename="<console>"
            , frame=None, EOF=None):
        u"""Starts a remote console

        The first argument is needed, it is the port number for the remote
        connection.

        .. code-block:: python

          def foo(arg1):
              ...
              RemoteConsole.run(4444) # terminal on port 4444

        The string 'EOF' ends the remote session.

        """
        frame = frame or inspect.currentframe().f_back
        if banner is None:
            banner = "console ...\n%s" % descrFrame(frame)
        if EOF:
            banner += "\nExit console with %r" % EOF
        if local_ns is None:
            local_ns = frame.f_locals
        if global_ns is None:
            global_ns = frame.f_globals
        #inspect.currentframe().f_back
        console = cls(local_ns, global_ns, filename)
        if EOF:
            banner += "\nExit console with %r" % EOF
            console.EOF = EOF
        console.interact(port, banner=banner)


# ==============================================================================
class Pdb(pdb.Pdb):  # pylint: disable=R0904
# ==============================================================================

    # pylint: disable=no-self-use, missing-docstring
    u"""Abstraction Layer for PDB"""
    def do_src(self, arg):
        if not arg:
            arg = 3
        six.print_(descrFrame(self.curframe, int(arg)))

    def help_src(self):
        six.print_("""show
Show source around current command (frame)
""")

    def do_console(self, arg):  # pylint: disable=W0613
        Console.run(frame=self.curframe, EOF='EOF')

    def help_console(self):
        six.print_("""console
run an interactive console in the current frame.
""")


# ==============================================================================
class RemotePdb(Pdb): # pylint: disable=R0904
# ==============================================================================
    u"""Simple remote PDB"""

    # pylint: disable=no-self-use, missing-docstring
    # pylint: disable=super-init-not-called
    def __init__(self, port, addr="127.0.0.1"):
        """Initialize the socket and initialize pdb."""

        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.old_stdin  = sys.stdin

        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.skt.bind((addr, port))
        self.skt.listen(1)
        ERROR("accept connection %s:%s" % (addr, port))
        (conn, self.remote) = self.skt.accept()
        ERROR("got connection from %s:%s" % self.remote)
        self.rwStream = conn.makefile('rw', 0)
        sys.stderr = sys.stdout = sys.stdin = self.rwStream
        Pdb.__init__(self, completekey='tab')
        ERROR("pdb inited")

    def shutdown(self):
        u"""shutdown PDB's' REPL"""
        try:
            self.rwStream.close()
        except Exception as exc: # pylint: disable=W0703
            ERROR("error on closing stream: " + str(exc))

        try:
            self.skt.close()
        except Exception as exc: # pylint: disable=W0703
            ERROR("error on closing socket: " + str(exc))

        ERROR("re-redirect")
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        sys.stdin  = self.old_stdin
        ERROR("close connection ...")
        self.set_continue()
        ERROR("connection %s:%s closed" % self.remote)

    def do_continue(self, arg):
        """Stop all operation on ``continue``."""
        self.shutdown()
        return 1

    do_EOF = do_quit = do_exit = do_c = do_cont = do_continue


# ==============================================================================
def trace(frame=None):
# ==============================================================================

    u"""A breakpoint starting a ``Pdb`` session.
    """
    frame = frame or inspect.currentframe().f_back
    Pdb().set_trace(frame=frame)

# ==============================================================================
def rtrace(port=4444, addr="127.0.0.1", frame=None):
# ==============================================================================

    u"""A breakpoint, starting a ``RemotePdb`` session. Default port ist 4444
    """
    frame = frame or inspect.currentframe().f_back
    RemotePdb(port, addr).set_trace(frame=frame)


# ==============================================================================
class DumpTelnet(Telnet):
# ==============================================================================

    u"""Inheritance fixing ``telnetlib.Telnet`` where it fails.
    """
    def listener(self):
        """Helper for mt_interact() -- this executes in the other thread."""
        while 1:
            try:
                data = self.read_eager()
            except EOFError:
                six.print_('*** Connection closed by remote host ***')
                return
            if data:
                if six.PY3:
                    sys.stdout.write(data.decode('ascii'))
                else:
                    sys.stdout.write(data)
            else:
                sys.stdout.flush()
            # without sleep cpu usage is 100%
            time.sleep(0.01)

# ==============================================================================
def rtrace_client(port=4444, addr="127.0.0.1", polltime=None):
# ==============================================================================
    u"""Set breakpoint for remote debugging"""
    while True:
        try:
            t = DumpTelnet(addr, port)
            t.interact()
            t.close()
        except Exception: # pylint: disable=broad-except
            pass
        if polltime is None:
            break
        time.sleep(polltime)


# def _test():
#     x = 12
#     rtrace()
#     x = 47
#     #RemoteConsole.run(4444)
#     #Console.run()
