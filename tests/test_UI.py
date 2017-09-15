# -*- coding: utf-8; mode: python -*-
"""test User Interface (sui)"""

from fspath.sui import SUI

#TMP = FSPath(OS_ENV.TEST_TEMPDIR)

def test_ask_choice():
    # within tox, stdin is redirected pseudofile and has no fileno()
    # How can we test SimpleUserInterface?
    pass

def interactive():
    l = ['January', 'February', 'March', 'April', 'May', 'June'
         , 'July', 'August', 'September', 'October', 'November', 'December']
    ret = SUI.ask_choice('select a month from the list.', l)
    print ('\n-->%s<--' % ret)
    SUI.write('----|')
    SUI.wait_key()
    ret = SUI.ask('how old are you?', default=20, count=3, echo=True, valid_chars=r'\d')
    print ('\n-->%s<--' % ret)
    ret = SUI.ask_yes_no('do you like coffee?')
    print('\n-->%s<--' % {SUI.YES:'yes', SUI.NO:'no'}[ret])

if __name__ == '__main__':
    interactive()
