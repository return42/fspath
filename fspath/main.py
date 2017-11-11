# -*- coding: utf-8; mode: python -*-

u"""fspath -- main entry point for commandline interfaces"""

import sys

from .cli import CLI
from .fspath import FSPath


def _cli_download_url(cli):
    u"""Download from 'url' into file 'fname'"""

    verbose = False
    try:
        verbose = cli.OUT.isatty()
    except AttributeError:
        pass
    verbose = (verbose and not cli.quiet)

    if cli.fname.EXISTS:
        raise cli.Error(42, "file %s already exists" % cli.fname)

    cli.fname.download(cli.url, chunksize=cli.chunksize, ticker=verbose, pipe=cli.OUT)
    if verbose:
        cli.OUT.write("download of '%s' succeed\n" % cli.fname)

def _cli_find_file(cli):
    u"""list file names matching regular expression

    To find e.g. all '.py' files in current folder use::

        fspath find ".*\\.py$"  .
    """
    for match in cli.folder.reMatchFind(
            cli.regexpr, use_dirs=(not cli.nodirs), use_files=(not cli.nofiles)):
        cli.OUT.write(match + "\n")

def _cli_extract(cli):
    u"""extract TAR or ZIP file"""
    verbose = False
    try:
        verbose = cli.OUT.isatty()
    except AttributeError:
        pass
    verbose = (verbose and not cli.quiet)
    cli.archive.extract(cli.folder, ticker=verbose)

# ==============================================================================
def main():
# ==============================================================================

    u"""
    Tools from the fspath library
    """
    cli = CLI(description=main.__doc__)

    from .win import _cli_py2exe
    py2exe = cli.addCMDParser(_cli_py2exe, cmdName='py2exe')
    py2exe.add_argument(
        "script"
        , type = FSPath
        , help = "pathname of the script to wrap")
    py2exe.add_argument(
        "--shebang"
        , type = str
        , default = "#!python.exe"
        , help = "shebang line")

    download = cli.addCMDParser(_cli_download_url, cmdName='download')
    download.add_argument(
        "fname"
        , type = FSPath
        , help = "name of the file")
    download.add_argument(
        "url"
        , type = str
        , help = "url of the content to download")

    download.add_argument(
        "--chunksize"
        , type  = int
        , default = 1048576
        , help = "download chunk size")

    download.add_argument(
        "-q", "--quiet"
        , action = 'store_true'
        , help   = "be quiet, no progressbar etc.")

    find = cli.addCMDParser(_cli_find_file, cmdName='find')
    find.add_argument(
        "--nofiles"
        , action = 'store_true'
        , help = "do not list file names")
    find.add_argument(
        "--nodirs"
        , action = 'store_true'
        , help = "do not list folder names")
    find.add_argument(
        "regexpr"
        , type = str
        , help = "regular expression")
    find.add_argument(
        "folder"
        , type = FSPath
        , nargs = "?"
        , default = FSPath(".")
        , help = "top folder")

    extract = cli.addCMDParser(_cli_extract, cmdName='extract')
    extract.add_argument(
        "archive"
        , type = FSPath
        , help = "file name of the TAR or ZIP archive")
    extract.add_argument(
        "folder"
        , type = FSPath
        , nargs = "?"
        , default = FSPath(".")
        , help = "extract into this folder")

    cli()

if __name__ == '__main__':
    sys.exit(main())
