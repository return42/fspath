# -*- coding: utf-8; mode: python -*-
"""test OS_ENV"""

from fspath import FSPath, OS_ENV
import os.path as osp
import os

def test_OS_ENV():
    OS_ENV.TMP = '/tmp/xyz'
    assert os.sep + osp.join('tmp', 'xyz') == FSPath('$TMP').EXPANDVARS
