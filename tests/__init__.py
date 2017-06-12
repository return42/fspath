#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    FSPath unit test driver
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright:  Copyright (C) 2017 Markus Heiser
    :license:    GPL Version 2, June 1991 see linux/COPYING for details.
"""

try:
    import os
    if os.environ.get("DEBUG", None):
        from pytest import set_trace
        __builtins__["DEBUG"] = set_trace
except ImportError:
    pass

if not os.environ.get("TEST_TEMPDIR"):
    os.environ["TEST_TEMPDIR"] = "tmp"

if not os.path.isdir(os.environ["TEST_TEMPDIR"]):
    os.mkdir(os.environ["TEST_TEMPDIR"])
