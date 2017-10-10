# -*- coding: utf-8; mode: python -*-
"""test User Interface (sui)"""

import time

from fspath.sui import SUI, CONSOLE_TYPE
from fspath.sui import ASCIITableFormatter, HTMLTableFormatter

#TMP = FSPath(OS_ENV.TEST_TEMPDIR)

test_rows = [  {'foo': 'foo <row 1>', 'bar': 'bar <row 1>'}
          , {'foo': 'foo <row 2>', 'bar': 'bar <row 2>'} ]

def test_ask_choice():
    # within tox, stdin is redirected pseudofile and has no fileno()
    # How can we test SimpleUserInterface?
    pass


def _test_choice():
    l = ['January', 'February', 'March', 'April', 'May', 'June'
         , 'July', 'August', 'September', 'October', 'November', 'December']
    ret = SUI.ask_choice('select a month from the list.', l)
    SUI.echo('-->%s<--' % ret)

def _test_wait_key():
    SUI.write('----|')
    SUI.wait_key()
    SUI.echo('OK')
    time.sleep(1)

def _test_ask():
    ret = SUI.ask('how old are you?', default=20, count=3, echo=True, valid_chars=r'\d')
    SUI.echo('-->%s<--' % ret)

def _test_ask_yes_no():
    ret = SUI.ask_yes_no('do you like coffee?')
    SUI.echo('-->%s<--' % {SUI.YES:'yes', SUI.NO:'no'}[ret])

def _test_fill_line():
    line_size = SUI._get_usable_line_size()
    for x in '12345':
        SUI.write(x * line_size)
        time.sleep(1)
        SUI.fill_line()

def _test_ascii_table_formatter():
    table = ASCIITableFormatter(("Foo",   "%-12s", "foo")
                                , ("Bar", "%-30s", "bar"))
    SUI.echo(table(test_rows))

def _test_html_table_formatter():
    table = HTMLTableFormatter(("Foo",   "%s", "foo")
                               , ("Bar", "%s", "bar"))
    SUI.echo(table(test_rows))

def _test_rst():
    SUI.rst_title("part's title", level='part')
    SUI.rst_p("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do"
              " eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut"
              " enim ad minim veniam quis nostrud exercitation ullamco laboris"
              " nisi ut aliquip ex ea commodo consequat.")
    SUI.rst_title("chapter's title")
    SUI.rst_p("""

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea

commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

  Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
""")
    SUI.rst_title("sections's title", level='section')
    SUI.rst_table(
        test_rows
        , ("Foo", "%-12s", "foo")
        , ("Bar", "%-30s", "bar"))
    time.sleep(1)

def _test_ask_fspath():
    ret = SUI.ask_fspath("enter path name / use [TAB] for complettion\npath: ")
    SUI.echo('-->%s<--' % ret)


def interactive():
    _test_ask_fspath()
    _test_choice()
    _test_wait_key()
    _test_ask()
    _test_ask_yes_no
    _test_fill_line()
    _test_ascii_table_formatter()
    _test_html_table_formatter()
    _test_rst()

if __name__ == '__main__':
    interactive()
