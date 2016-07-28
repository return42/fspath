# -*- coding: utf-8; mode: python -*-
u"""
Handling path names and executables more comfortable.
"""

# ==============================================================================
# imports
# ==============================================================================

import io
import os
from os import path
import re
import shutil
import subprocess
import sys
from glob import iglob
from contextlib import closing

import six
from six.moves.urllib.request import urlopen # pylint: disable=E0401

from .progressbar import progressbar, humanizeBytes

# ==============================================================================
class FSPath(six.text_type):
# ==============================================================================

    u"""
    A path name to a file or folder.

    Handling path names more comfortable, e.g.:

    * concatenate path names with the division operator ``/``
    * call functions like *mkdir* on path names
    * get properties like *EXISTS*

    .. code-block:: python

       >>> folder = fspath.FSPath("/tmp")
       >>> folder.EXISTS
       True
       >>> (folder / "subfolder").makedirs()
       >>> list(folder.reMatchFind(".*sub"))
       ['/tmp/subfolder']
       >>> (folder / "test.txt").FILENAME
       'test'
       >>> (folder / "test.txt").DIRNAME
       '/tmp'
       >>> six.print_("topfolder" / folder)
       topfolder/temp
       >>> six.print_(folder + "addedstr")
       tmpaddedstr
       >>> six.print_((folder/"foo"/"bar.txt").splitpath())
       (u'/tmp/foo', u'bar.txt')
       >>> six.print_(folder / "foo" / "../bar.txt")
       tmp/bar.txt
    """

    def __new__(cls, pathname):
        u"""Constructor of a path name object.

        Regardless of how the encoding of the file system is, the ``pathname``
        is converted to unicode. The conversion of byte strings is based the
        default encodings.

        To issue "File-system Encoding" See also:

        * https://docs.python.org/3.5/howto/unicode.html#unicode-filenames
        """
        pathname = path.normpath(path.expanduser(six.text_type(pathname)))
        return super(FSPath, cls).__new__(cls, pathname)

    @property
    def VALUE(self):
        u"""string of the path name"""
        return six.text_type(self)

    @property
    def EXISTS(self):
        u"""True if file/pathname exist"""
        return path.exists(self)

    @property
    def SIZE(self):
        u"""Size in bytes"""
        return path.getsize(self)

    @property
    def isReadable(self):
        u"""True if file/path is readable"""
        return os.access(self, os.R_OK)

    @property
    def isWriteable(self):
        u"""True if file/path is writeable"""
        return os.access(self, os.W_OK)

    @property
    def isExecutable(self):
        u"""True if file is executable"""
        return os.access(self, os.X_OK)

    @property
    def ISDIR(self):
        u"""True if path is a folder"""
        return path.isdir(self)

    @property
    def ISFILE(self):
        u"""True if path is a file"""
        return path.isfile(self)

    @property
    def ISLINK(self):
        u"""True if path is a symbolic link"""
        return path.islink(self)

    @property
    def DIRNAME(self):
        u"""The path name of the folder, where the file is located

        E.g.: ``/path/to/folder/filename.ext`` --> ``/path/to/folder``
        """
        return self.__class__(path.dirname(self))

    @property
    def BASENAME(self):
        u"""The path name with suffix, but without the folder name.

        E.g.: ``/path/to/folder/filename.ext`` --> ``filename.ext``
        """
        return self.__class__(path.basename(self))

    @property
    def FILENAME(self):
        u"""The path name without folder and suffix.

        E.g.: ``/path/to/folder/filename.ext`` --> ``filename``

        """
        return self.__class__(path.splitext(path.basename(self))[0])

    @property
    def SUFFIX(self):
        u"""The filename suffix

        E.g.: ``/path/to/folder/filename.ext`` --> ``.ext``

        """
        return self.__class__(path.splitext(self)[1])

    @property
    def SKIPSUFFIX(self):
        u"""The complete file name without suffix.

        E.g.: ``/path/to/folder/filename.ext`` --> ``/path/to/folder/filename``
        """
        return self.__class__(path.splitext(self)[0])

    @property
    def ABSPATH(self):
        u"""The absolute pathname

        E.g: ``../to/../to/folder/filename.ext`` --> ``/path/to/folder/filename.ext``

        """
        return self.__class__(path.abspath(self))

    @property
    def REALPATH(self):
        u"""The real pathname without symbolic links."""
        return self.__class__(path.realpath(self))

    @property
    def POSIXPATH(self):
        u"""The path name in *POSIX* notation.

        Helpfull if you are on MS-Windows and need the POSIX name.
        """
        if os.sep == "/":
            return six.text_type(self)
        else:
            p = six.text_type(self)
            if p[1] == ":":
                p = "/" + p.replace(":", "", 1)
            return p.replace(os.sep, "/")

    @property
    def NTPATH(self):
        u"""The path name in the Windows (NT) notation.
        """
        if os.sep == "\\":
            return six.text_type(self)
        else:
            return six.text_type(self).replace(os.sep, "\\")

    @property
    def EXPANDVARS(self):
        u"""Path with environment variables expanded."""
        return self.__class__(path.expandvars(self))

    @property
    def EXPANDUSER(self):
        u"""Path with an initial component of ~ or ~user replaced by that user's home."""
        return self.__class__(path.expanduser(self))

    @classmethod
    def getHOME(cls):
        u"""User's home folder."""
        return cls(path.expanduser("~"))

    def makedirs(self, mode=0o775):
        u"""Recursive directory creation, default mode is 0o775 (octal)."""
        if not self.ISDIR:
            return os.makedirs(self, mode)

    def __div__(self, pathname):
        return self.__class__(self.VALUE + os.sep + six.text_type(pathname))
    __truediv__ = __div__

    def __rdiv__(self, pathname):
        return self.__class__(six.text_type(pathname) + os.sep + self.VALUE)

    def __add__(self, other):
        return self.__class__(self.VALUE + six.text_type(other))

    def __radd__(self, other):
        return self.__class__(six.text_type(other) + self.VALUE)

    def relpath(self, start):
        return self.__class__(path.relpath(self, start))

    def splitpath(self):
        head, tail = path.split(self)
        return (self.__class__(head), self.__class__(tail))

    def listdir(self):
        for name in os.listdir(self):
            yield self.__class__(name)

    def glob(self, pattern):
        for name in  iglob(self / pattern ):
            yield self.__class__(name)

    def walk(self, topdown=True, onerror=None, followlinks=False):
        for dirpath, dirnames, filenames in os.walk(self, topdown, onerror, followlinks):
            yield (self.__class__(dirpath)
                   , [self.__class__(x) for x in dirnames]
                   , [self.__class__(x) for x in filenames]
            )

    def reMatchFind(self, name, isFile=True, isDir=True, followlinks=False):

        # find first e.g: next(myFolder.reMatchFind(r".*name.*"), None)

        name_re = re.compile(name)
        for folder, dirnames, filenames in self.walk(followlinks=followlinks):
            if isDir:
                for d_name in [x for x in dirnames if name_re.match(x)]:
                    yield folder / d_name
            if isFile:
                for f_name in [x for x in filenames if name_re.match(x)]:
                    yield folder / f_name

    def suffix(self, newSuffix):
        return self.__class__(self.SKIPSUFFIX + newSuffix)

    def copyfile(self, dest, preserve=False):
        u"""Copy the file src to the file or directory dest.

        Argument preserve copies permission bits.
        """
        if preserve:
            shutil.copy2(self, dest)
        else:
            shutil.copy(self, dest)

    def copytree(self, dest, symlinks=False, ignore=None):
        u"""Recursively copy the entire directory tree"""
        shutil.copytree(self, dest, symlinks, ignore)

    def move(self, dest):
        u"""Move path to another location (dest)"""
        shutil.move(self, dest)

    def delete(self):
        u"""remove file/folder"""
        if self.ISDIR:
            self.rmtree()
        else:
            os.remove(self)

    def rmtree(self, ignore_errors=False, onerror=None):
        u"""remove tree"""
        shutil.rmtree(self, ignore_errors, onerror)

    def filesize(self, precision=None):
        u"""Filesize in bytes or with precision"""
        size = path.getsize(self)
        if precision is not None:
            size = humanizeBytes(size, precision)
        return size

    def openTextFile(
            self, mode = 'r', encoding = 'utf-8'
            , errors = 'strict', buffering = 1
            , newline = None):
        u"""Open file as text file"""
        return io.open(
            self, mode=mode, encoding=encoding
            , errors=errors, buffering=buffering
            , newline=newline)

    def readFile(self, encoding='utf-8', errors='strict'):
        u"""read entire file"""
        with self.openTextFile(encoding=encoding, errors=errors) as f:
            return f.read()

    def Popen(self, *args, **kwargs):
        u"""Get a ``subprocess.Popen`` object (``proc``).

        The path name of the self-object is the programm to call. The program
        arguments are given py ``*args`` and the ``*kwargs`` are passed to the
        ``subprocess.Popen`` constructor. The ``universal_newlines=True`` is
        true by default.

        see https://docs.python.org/3/library/subprocess.html#popen-constructor

        .. code-block:: python

           import six
           from fspath import FSPath
           proc = FSPath("arp").Popen("-a",)
           stdout, stderr = proc.communicate()
           retVal = proc.returncode
           six.print_("stdout: %s" % stdout)
           six.print_("stderr: %s" % stderr)
           six.print_("exit code = %d" % retVal)

        """

        defaults = {
            'stdout'               : subprocess.PIPE
            , 'stderr'             : subprocess.PIPE
            , 'stdin'              : subprocess.PIPE
            , 'universal_newlines' : True
            }
        defaults.update(kwargs)
        return subprocess.Popen([self,] + list(args), **defaults)

    def download(self, url, chunkSize=1048576, ticker=False):
        u"""Download URL into file

        The default chunkSize is 1048576 Bytes, with ticker=True an progress-bar
        is prompted."""

        downBytes  = 0
        totalBytes = 0

        def __ticker():
            if ticker and totalBytes:
                progressbar(downBytes, totalBytes, prompt = prompt)

        with open(self, "wb") as f:
            with closing(urlopen(url)) as d:
                totalBytes = int(d.headers.get("Content-Length", 0))
                if chunkSize is None:
                    chunkSize = totalBytes // 100
                prompt = "%s: [%s]" % (
                    self, humanizeBytes(totalBytes, 1))
                __ticker()
                while 1:
                    x = d.read(chunkSize)
                    if not len(x):
                        break
                    f.write(x)
                    downBytes += len(x)
                    __ticker()

# ==============================================================================
def which(fname, findall=True):
# ==============================================================================
    u"""
    Searches the fname in the enviroment ``PATH``.

    This *which* is not POSIX conform, it searches the fname (without extension)
    and the fname with one of the ".exe", ".cmd", ".bat" extension. If nothing
    is found, ``None` is returned if something matches, a list (``set``) is
    returned. With option ``findall=False`` the first match is returned or
    ``None``, if nothing is found.
    """
    exe = ["", ".exe", ".cmd", ".bat"]
    if sys.platform != 'win32':
        exe = [""]
    envpath = os.environ.get('PATH', None) or os.defpath

    locations = set()
    for folder in envpath.split(os.pathsep):
        for ext in exe:
            fullname = FSPath(folder + os.sep + fname + ext)
            if fullname.ISFILE:
                if not findall:
                    return fullname
                locations.add(fullname)
    return locations or None

# ==============================================================================
def callEXE(cmd, *args, **kwargs):
# ==============================================================================

    u"""
    Synchronous command call ``cmd`` with arguments ``*args`` .

    The ``*kwargs`` are passed to the ``subprocess.Popen`` constructor. The
    return value is a three-digit tuple ``(stdout, stderr, rc)``.

    .. code-block:: python

       import six
       from fspath import callEXE
       out, err, rc = callEXE("arp", "-a")

       six.print_("stdout: %s" % out)
       six.print_("stderr: %s" % err)
       six.print_("exit code = %d" % rc)
    """

    exe = which(cmd, findall=False)
    if exe is None:
        raise IOError('command "%s" not availble!' % cmd)
    proc = exe.Popen(*args, **kwargs)
    stdout, stderr = proc.communicate()
    rc = proc.returncode
    return (stdout, stderr, rc)


# ==============================================================================
class DevNull(object):
# ==============================================================================

    """A dev/null file descriptor."""
    def write(self, *args, **kwargs):
        pass

DevNull = DevNull()
