=================================================
fspath enjoy pathes
=================================================

.. revealjs:: the joy of python programming
   :data-transition: linear

   .. rv_small::

      *Hit '?' to see keyboard shortcuts*

   `fspath@GitHub <https://github.com/return42/fspath>`_

   .. rv_small::

      contributed by `return42 <http://github.com/return42>`_



.. revealjs:: tired in os.path?
   :title-heading: h2

   .. rv_small::

      are you tired in juggling with

   .. rv_code::

      parent_dir = os.path.abspath(
                       os.path.join(
                           os.path.dirname(__file__)
                           , os.path.pardir))

   .. rv_small::

      ... and all that blody stuff? do you think this ..

   .. rv_code::

      parent_dir = FSPath(__file__).DIRNAME.ABSPATH / ".."

   .. rv_small::

      is much readable?

   ... then continue.


.. revealjs:: Verweise
   :title-heading: h2

   This slide show was build with the help of ..

   .. rv_small::

      - `sphinxjp.themes.revealjs <https://github.com/tell-k/sphinxjp.themes.revealjs>`_
      - `REVEAL.JS <http://lab.hakim.se/reveal-js>`_
      - `Sphinx-doc <http://www.sphinx-doc.org>`_
      - `reST <http://www.sphinx-doc.org/en/stable/rest.html>`_
      - `docutils <http://docutils.sourceforge.net/rst.html>`_
