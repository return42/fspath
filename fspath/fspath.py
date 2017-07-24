# -*- coding: utf-8; mode: python -*-
u"""
Handling path names and executables more comfortable.
"""

# pylint: disable=bad-continuation

# ==============================================================================
# imports
# ==============================================================================

import sys
import io
import os
from os import path
import platform
import re
import shutil
import subprocess
from glob import iglob
from contextlib import closing
import zipfile
import tarfile

import six
from six.moves.urllib.request import urlopen # pylint: disable=E0401

from .progressbar import progressbar, humanizeBytes
from .helper import Options

# ==============================================================================
class FSPath(six.text_type):  # pylint: disable=too-many-public-methods
# ==============================================================================

    u"""
    A path name to a file or folder.

    Handling path names more comfortable, e.g.:

    * concatenate path names with the division operator ``/``
    * call functions like *mkdir* on path names
    * get properties like *EXISTS*

    .. code-block:: python

      >>> from fspath import FSPath
      >>> tmp = FSPath('~/tmp')
      >>> tmp
      '/home/user/tmp'
      >>> tmp.EXISTS
      False

    no additional import, no juggling with ``os.join(...)``

    simply slash ``/`` and ``foo.<method>`` calls

    .. code-block:: python

      >>> [(tmp/x).makedirs() for x in ('foo', 'bar')]
      True, True
      >>> for n in tmp.listdir():
      ...     print(tmp / n)
      ...
      /home/user/tmp/foo
      /home/user/tmp/bar

    downloads & archives

    .. code-block:: python

      >>> arch = foo / 'fspath.zip'
      >>> url = 'https://github.com/return42/fspath/archive/master.zip'

   ``download`` -- super easy download + segmentation + nice ticker

    .. code-block:: python

      >>> arch.download(url, chunkSize=1024, ticker=True)
      /home/user/tmp/foo/fspath.zip: [87.9 KB][===============    ]  83%

   ``FSPath.extract`` -- extract in one step, no matter ZIP or TAR

    .. code-block:: python

      >>> arch.ISTAR, arch.ISZIP
      (False, True)
      >>> arch.extract(foo)
      ['fspath-master/', 'fspath-master/.gitignore'
      , 'fspath-master/MAINFEST.in', 'fspath-master/Makefile'
      , 'fspath-master/README.rst',  ... ]

    For more examples see our `slide-show <../slides/index.html>`_.

    """

    OS = Options(
        sep       = os.sep     # https://docs.python.org/3/library/os.html#os.sep
        , curdir  = os.curdir  # https://docs.python.org/3/library/os.html#os.curdir
        , altsep  = os.altsep  # https://docs.python.org/3/library/os.html#os.altsep
        , extsep  = os.extsep  # https://docs.python.org/3/library/os.html#os.extsep
        , pathsep = os.pathsep # https://docs.python.org/3/library/os.html#os.pathsep
        , defpath = os.defpath # https://docs.python.org/3/library/os.html#os.defpath
        , linesep = os.linesep # https://docs.python.org/3/library/os.html#os.linesep
        , devnull = os.devnull # https://docs.python.org/3/library/os.html#os.devnull    
    )
        
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
    def READABLE(self):
        u"""True if file/path is readable"""
        return os.access(self, os.R_OK)

    @property
    def WRITEABLE(self):
        u"""True if file/path is writeable"""
        return os.access(self, os.W_OK)

    @property
    def EXECUTABLE(self):
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
    def ISABSPATH(self):
        u"""True if path is absolute"""
        return path.isabs(self)

    @property
    def ISLINK(self):
        u"""True if path is a symbolic link"""
        return path.islink(self)

    @property
    def ISMOUNT(self):
        u"""True if path is a mountpoint"""
        return path.ismount(self)

    @property
    def MTIME(self):
        """Return the last modification time, reported by os.stat()."""
        return os.stat(self).st_mtime

    @property
    def ATIME(self):
        """Return the last access time, reported by os.stat()."""
        return os.stat(self).st_atime

    @property
    def CTIME(self):
        """Return the metadata change time, reported by os.stat()."""
        return os.stat(self).st_ctime

    @property
    def ISZIP(self):
        u"""True if path is a ZIP file"""
        return zipfile.is_zipfile(self)

    @property
    def ISTAR(self):
        u"""True if path is a TAR archive file"""
        return tarfile.is_tarfile(self)

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
        retVal = None
        if os.sep == "\\":
            retVal = six.text_type(self)
        else:
            retVal = six.text_type(self).replace(os.sep, "\\")
        return retVal

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

    @classmethod
    def getCWD(cls):
        u"""Current working directory."""
        return cls(os.getcwd())

    def chdir(self):
        u"""change the current working directory to *self*."""
        os.chdir(self)

    def makedirs(self, mode=0o775):
        u"""Recursive directory creation, default mode is 0o775 (octal).

        :param int mode: file permissons
        :return: created (True) already exists (True),
        :raises Exception: in case of errors (permissons, etc.)
        """
        retVal = False
        if not self.ISDIR:
            os.makedirs(self, mode)
            retVal = True
        return retVal

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
        u"""Return a relative version of a path"""
        return self.__class__(path.relpath(self, start))

    def splitpath(self):
        u"""Split a pathname.

        Return tuple (head, tail) where tail is everything after the final
        slash.  Either part may be empty."""
        head, tail = path.split(self)
        return (self.__class__(head), self.__class__(tail))

    def listdir(self):
        u"""Return a iterator which yields the names of the files in the directory."""
        for name in os.listdir(self):
            yield self.__class__(name)

    def glob(self, pattern, relpath=False):
        u"""Return an iterator which yields the paths matching a pathname pattern.

        The pattern may contain simple shell-style wildcards a la
        fnmatch. However, unlike fnmatch, filenames starting with a dot are
        special cases that are not matched by '*' and '?'  patterns.
        """
        for name in  iglob(self / pattern):
            obj = self.__class__(name)
            if relpath is True:
                obj = obj.relpath(self)
            yield obj

    def walk(self, topdown=True, onerror=None, followlinks=False):
        u"""Directory tree generator.

        For each directory in the directory tree rooted at top (including top
        itself, but excluding '.' and '..'), yields a 3-tuple::

            folder, dirnames, filenames

        dirnames is a list of the names of the subdirectories in dirpath
        (excluding '.' and '..').  filenames is a list of the names of the
        non-directory files in dirpath.

        Note that the names in the lists are just names, with no path components.
        To get a full path (which begins with top) to a file or directory in
        dirpath, do ``folder / name``.

        By default, os.walk does not follow symbolic links to subdirectories on
        systems that support them.  In order to get this functionality, set the
        optional argument 'followlinks' to true.

        .. caution::

           If you pass a relative pathname for top, don't change the current
           working directory between resumptions of walk.  walk never changes
           the current directory, and assumes that the client doesn't either.

        For more details see ``os.walk``"""

        # argh those fu.. idiots from python impleted fspath in 3.4 which no
        # longer supports string-like objects (inheritance of str) in os.walk.
        # So we have to typecast str(self).
        for dirpath, dirnames, filenames in os.walk(str(self), topdown, onerror, followlinks):
            yield (self.__class__(dirpath)
                   , [self.__class__(x) for x in dirnames]
                   , [self.__class__(x) for x in filenames])

    def reMatchFind(self, name, isFile=True, isDir=True, followlinks=False, relpath=False):
        u"""Returns iterator which yields matching path names

        :param isFile:      iterator includes names of files
        :param isDir:       iterator includes names of folders
        :param followlinks: follow symbolic links

        To find all C and header files use::

            folder.reMatchFind("*\\.[ch]")

        To find the first C or header file use::

            next(myFolder.reMatchFind("*\\.[ch]"), None)
        """

        name_re = re.compile(name)
        for folder, dirnames, filenames in self.walk(followlinks=followlinks):
            if isDir:
                for d_name in [x for x in dirnames if name_re.match(x)]:
                    obj = folder / d_name
                    if relpath:
                        obj = obj.relpath(self)
                    yield obj
            if isFile:
                for f_name in [x for x in filenames if name_re.match(x)]:
                    obj = folder / f_name
                    if relpath:
                        obj = obj.relpath(self)
                    yield obj

    def suffix(self, newSuffix):
        u"""Return path name with ``newSuffix``"""
        return self.__class__(self.SKIPSUFFIX + newSuffix)

    def copyfile(self, dest, preserve=False):
        u"""Copy the file src to the file or directory dest.

        :dest str: The destination may be a directory
        :preserve bool: copies permission bits
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
        return self.__class__(dest)

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

    def openTextFile(self
                     , mode='rt', encoding='utf-8'
                     , errors='strict', buffering=1
                     , newline=None):
        u"""Open file as text file.

        wraps `io.open <https://docs.python.org/library/io.html#io.open>`_:

        * except argument ``closefd`` (meaningless when using filenames)
        * ``encoding='utf-8'`` is default
        * ``mode='rt'`` is default
        * ``buffering=1`` is default (selects line buffering)
        """
        return io.open(self
                       , mode=mode, encoding=encoding
                       , errors=errors, buffering=buffering
                       , newline=newline)

    def openBinaryFile(self, mode='rb', errors='strict', buffering=None):
        u"""Open file as binary file.

        wraps `io.open <https://docs.python.org/library/io.html#io.open>`_:

        * except argument ``closefd`` (meaningless when using filenames)
        * except argument ``encoding`` (meaningless since *binary*)
        * except argument ``newline`` (meaningless since *binary*)
        * ``mode='rb'`` is default
        """
        return io.open(self, mode=mode, errors=errors, buffering=buffering)

    def startFile(self):
        """Start a file with its associated application."""
        system  = platform.system()
        if system == 'Windows':
            os.startfile(self)
            return
        cmd = 'xdg-open'
        if system in ('FreeBSD', 'Darwin'):
            cmd = 'open'

        from ._which import which
        cmd = which(cmd, findall=False)
        if cmd:
            os.system(cmd + " " + self)
        
    def readFile(self, encoding='utf-8', errors='strict'):
        u"""read entire file"""
        with self.openTextFile(encoding=encoding, errors=errors) as f:
            return f.read()

    def extract(self, folder=".", pwd=None):
        u"""Extract TAR or ZIP archive to 'folder'

        Uses ``extractall`` from :py:class:`tarfile.TarFile` and
        :py:class:`zipfile.Zipfile` to extract into ``folder``.

        :folder str: folder to extract into
        :pwd str: password for crypted (only ZIP)
        :return: members in an iterable form (list or just iterator)
        """
        folder = self.__class__(folder)
        if not folder.EXISTS:
            folder.makedirs()
        members = None
        if self.ISTAR:
            # pylint: disable=redefined-variable-type
            arc = tarfile.TarFile(self)
            members = arc
            arc.extractall(path=str(folder.ABSPATH), members=members)

        elif self.ISZIP:
            # pylint: disable=redefined-variable-type
            arc = zipfile.ZipFile(self)
            members = arc.namelist()
            arc.extractall(str(folder.ABSPATH), members , pwd)

        else:
            raise tarfile.ExtractError("%s archive type is unknown" % self)
        return members


    def Popen(self, *args, **kwargs):  # pylint: disable=invalid-name
        u"""Get a ``subprocess.Popen`` object (``proc``).

        The path name of the self-object is the programm to call. The program
        arguments are given py ``*args`` and the ``*kwargs`` are passed to the
        ``subprocess.Popen`` constructor. The ``universal_newlines=True`` is
        true by default.

        see https://docs.python.org/3/library/subprocess.html#popen-constructor

        .. code-block:: python

           from fspath import FSPath
           proc = FSPath("arp").Popen("-a",)
           stdout, stderr = proc.communicate()
           retVal = proc.returncode
           print("stdout: %s" % stdout)
           print("stderr: %s" % stderr)
           print("exit code = %d" % retVal)

        """

        defaults = {
            'stdout'               : subprocess.PIPE
            , 'stderr'             : subprocess.PIPE
            , 'stdin'              : subprocess.PIPE
            , 'universal_newlines' : True
            }
        defaults.update(kwargs)
        return subprocess.Popen([self,] + list(args), **defaults)

    def download(self, url, chunkSize=1048576, ticker=False, pipe=sys.stdout):
        u"""Download URL into file

        The default chunkSize is 1048576 Bytes, with ticker=True an progress-bar
        is prompted.

        E.g. to download FSPath's README.rst with a progressbar on stdout::

            url = "https://raw.githubusercontent.com/return42/fspath/master/README.rst"

            readme = FSPath("README.rst")
            readme.download(url, ticker=True)
        """

        downBytes  = 0
        totalBytes = 0

        def __ticker():
            if ticker and totalBytes:
                progressbar(downBytes, totalBytes, prompt=prompt, pipe=pipe)

        with closing(urlopen(url)) as d:
            with open(self, "wb") as f:
                # pylint: disable=no-member
                totalBytes = int(d.headers.get("Content-Length", 0))
                if chunkSize is None:
                    chunkSize = totalBytes // 100
                prompt = "%s: [%s]" % (
                    self, humanizeBytes(totalBytes, 1))
                __ticker()
                while 1:
                    x = d.read(chunkSize)
                    if not bool(len(x)):
                        break
                    f.write(x)
                    downBytes += len(x)
                    __ticker()
                if ticker:
                    pipe.write('\n')


# ==============================================================================
def callEXE(cmd, *args, **kwargs):
# ==============================================================================

    u"""
    Synchronous command call ``cmd`` with arguments ``*args`` .

    The ``*kwargs`` are passed to the ``subprocess.Popen`` constructor. The
    return value is a three-digit tuple ``(stdout, stderr, rc)``.

    .. code-block:: python

       from fspath import callEXE
       out, err, rc = callEXE("arp", "-a")

       print("stdout: %s" % out)
       print("stderr: %s" % err)
       print("exit code = %d" % rc)
    """
    from ._which import which
    exe = which(cmd, findall=False)
    if exe is None:
        raise IOError('command "%s" not availble!' % cmd)
    proc = exe.Popen(*args, **kwargs)
    stdout, stderr = proc.communicate()
    retVal = proc.returncode
    return (stdout, stderr, retVal)


# ==============================================================================
class DevNull(object): # pylint: disable=too-few-public-methods
# ==============================================================================

    """A dev/null file descriptor."""
    def write(self, *args, **kwargs):
        u"""writer which writes nothing"""
        pass

DevNull = DevNull() # pylint: disable=invalid-name
