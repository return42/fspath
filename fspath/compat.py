# -*- coding: utf-8; mode: python -*-
"""
Stuff for Python version compatibility.
"""
# pylint: disable=superfluous-parens,missing-docstring,missing-docstring

from six import PY3

# indent()
if PY3:
    from textwrap import indent               # pylint: disable=unused-import
else:
    # backport from python3
    def indent(text, prefix, predicate=None): # pylint: disable=function-redefined
        # type: (unicode, unicode, Callable) -> unicode
        if predicate is None:
            def predicate(line):              # pylint: disable=function-redefined
                # type: (unicode) -> unicode
                return line.strip()

        def prefixed_lines():
            # type: () -> Generator
            for line in text.splitlines(True):
                yield (prefix + line if predicate(line) else line)
        return ''.join(prefixed_lines())

