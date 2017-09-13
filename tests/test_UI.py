# -*- coding: utf-8; mode: python -*-
"""test User Interface (sui)"""

from fspath.sui import SUI

#TMP = FSPath(OS_ENV.TEST_TEMPDIR)

def test_ask_choice():
    l = ['January', 'February', 'March', 'April', 'May', 'June'
         , 'July', 'August', 'September', 'October', 'November', 'December']

    # within tox, stdin is redirected pseudofile and has no fileno()
    # How can we test SimpleUserInterface?
    #month = SUI.ask_choice('select a month from the list.', l)

