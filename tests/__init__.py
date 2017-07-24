# -*- coding: utf-8; mode: python -*-
"""fspath unit test driver"""

import os

try:
    if os.environ.get("DEBUG", None):
        from pytest import set_trace
        __builtins__["DEBUG"] = set_trace
except ImportError:
    pass

build_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__)
        , os.path.pardir)) + os.sep + 'build'

os.environ["TEST_TEMPDIR"] = build_dir + os.sep + 'tmp'

if not os.path.isdir(os.environ["TEST_TEMPDIR"]):
    os.mkdir(os.environ["TEST_TEMPDIR"])
