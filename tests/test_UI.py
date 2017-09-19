# -*- coding: utf-8; mode: python -*-
"""test User Interface (sui)"""

import time

from fspath.sui import SUI, CONSOLE_TYPE
from fspath.sui import ASCIITableFormatter, HTMLTableFormatter

#TMP = FSPath(OS_ENV.TEST_TEMPDIR)

def test_ask_choice():
    # within tox, stdin is redirected pseudofile and has no fileno()
    # How can we test SimpleUserInterface?
    pass


def _test_choice():
    l = ['January', 'February', 'March', 'April', 'May', 'June'
         , 'July', 'August', 'September', 'October', 'November', 'December']
    ret = SUI.ask_choice('select a month from the list.', l)
    SUI.echo('\n-->%s<--' % ret)

def _test_wait_key():
    SUI.write('----|')
    SUI.wait_key()
    SUI.echo('OK')
    time.sleep(1)

def _test_ask():
    ret = SUI.ask('how old are you?', default=20, count=3, echo=True, valid_chars=r'\d')
    SUI.echo('\n-->%s<--' % ret)

def _test_ask_yes_no():
    ret = SUI.ask_yes_no('do you like coffee?')
    print('\n-->%s<--' % {SUI.YES:'yes', SUI.NO:'no'}[ret])

def _test_fill_line():
    line_size = SUI._get_usable_line_size()
    for x in '12345':
        SUI.write(x * line_size)
        time.sleep(1)
        SUI.fill_line()

def _test_ascii_table_formatter():
    rows = [  {'foo': 'foo row 1', 'bar': 'bar row 1'}
              , {'foo': 'foo row 2', 'bar': 'bar row 2'} ]

    table = ASCIITableFormatter(("Foo",   "%-12s", "foo")
                                , ("Bar", "%-30s",  "bar"))
    SUI.echo(table(rows))

def _test_html_table_formatter():
    rows = [  {'foo': 'foo <row 1>', 'bar': 'bar <row 1>'}
              , {'foo': 'foo <row 2>', 'bar': 'bar <row 2>'} ]

    table = HTMLTableFormatter(("Foo",   "%s", "foo")
                               , ("Bar", "%s", "bar"))
    SUI.echo(table(rows))

def interactive():
    _test_ascii_table_formatter()
    _test_html_table_formatter()

    _test_choice()
    _test_wait_key()
    _test_ask()
    _test_ask_yes_no
    _test_fill_line()

if __name__ == '__main__':
    interactive()
