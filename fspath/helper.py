# -*- coding: utf-8; mode: python -*-
u"""
nothing special here, just some small helper
"""
# pylint: disable=too-many-instance-attributes

# ==============================================================================
class Options(dict):
# ==============================================================================
    u"""A container to hold *options*

    .. code-block:: python

      >>> x = Options(x='foo', y='bar')
      >>> x.get("z", 'not available')
      not available
      >>> x.y
      bar
    """

    @property
    def __dict__(self):
        u"""Emulate the ``self.__dict__`` of an ``object`` type.
        """
        return self

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, val):
        self[attr] = val

# ==============================================================================
class OptionsWithDefault(Options):
# ==============================================================================

    u"""A container to hold *options* with defaults

    Kann mit einem Python-Dictionary oder Keyword-Argumneten im Konstruktor
    beladen werden. Verwendungszweck sehr allgemein, z.B.:

    ..codeblock:: python

      >>> x = OptionsWithDefault('unknown', x='foo', y='bar')
      >>> x.z
      'unknown'
      >>> x.y
      'bar'
    """

    def __init__(self, default, *args, **kwargs):
        self["__default"] = default
        Options.__init__(self, *args, **kwargs)

    def __getattr__(self, attr):
        return self.get(attr, self["__default"])
