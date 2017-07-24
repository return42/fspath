# -*- coding: utf-8; mode: python -*-

"""foobar CLI"""

import sys
from fspath import CLI, FSPath

def cli_hello(cliArgs):
    """another 'hello world'"""
    print('hello world')

def cli_dir(cliArgs):
    """list directory"""
    for f in cliArgs.folder.listdir():
        l = f.upper() if cliArgs.upper else f
        f = cliArgs.folder / f
        if cliArgs.verbose:
            l = '[%10s] ' % (f.filesize(precision=0)) + l  
        print(l, end = ('\n' if cliArgs.verbose else ', '))


def main():
    # define CLI
    cli = CLI(description=main.__doc__)

    hello = cli.addCMDParser(cli_hello, cmdName='hello')

    listdir = cli.addCMDParser(cli_dir, cmdName='dir')
    listdir.add_argument(
        "folder", type = FSPath
        , nargs = "?", default = FSPath(".")
        , help = "path of the folder")
    listdir.add_argument(
        "--upper", action = 'store_true'
        , help = "convert to upper letters")
    # run CLI
    cli()

if __name__ == '__main__':
    sys.exit(main())


