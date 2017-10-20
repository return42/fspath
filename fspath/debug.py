#!/usr/bin/env python
# -*- coding: utf-8; mode: python -*-
# pylint: disable=invalid-name

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

from code   import InteractiveConsole
from codeop import CommandCompiler
from telnetlib import Telnet
import six

__all__ = ['Console', 'RemoteConsole', 'RemotePdb', 'rtrace', 'trace']

# ==============================================================================
def ERROR(msg): # pylint: disable=C0103
# ==============================================================================

    sys.__stderr__.write(msg + "\n")
    sys.__stderr__.flush()

# ==============================================================================
def descrFrame(frame, arround=3):
# ==============================================================================

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
        else:
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
        except SystemExit:
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

    def interact(self, port, banner=None):
        addr = socket.gethostname()

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
        #ERROR("redirect")
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
    def run(cls, port, local_ns=None, global_ns=None
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

    def __init__(self, port):
        """Initialize the socket and initialize pdb."""
        addr = socket.gethostname()

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
        pdb.Pdb.__init__(self, completekey='tab')
        ERROR("pdb inited")

    def shutdown(self):

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
def rtrace(port=4444, frame=None):
# ==============================================================================

    u"""A breakpoint, starting a ``RemotePdb`` session. Default port ist 4444
    """
    frame = frame or inspect.currentframe().f_back
    RemotePdb(port).set_trace(frame=frame)

# ==============================================================================
def rtrace_client(host=socket.gethostname(), port=4444, polltime=None):
# ==============================================================================

    ERROR("open telnet session to host '%s' port '%s'" % (host,port))
    while True:
        try:
            t = Telnet(host, port)
            t.interact()
            t.close()
        except Exception:
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
