# -*- coding: utf-8; mode: python -*-
"""test OS_ENV"""

from fspath import FSPath, OS_ENV

def test_OS_ENV():
    OS_ENV.TMP = '/tmp/xyz'
    assert '/tmp/xyz' == FSPath('$TMP').EXPANDVARS
