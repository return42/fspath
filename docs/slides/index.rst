=================================================
enjoy in scripting
=================================================

.. raw:: html

   <aside id="logo" style="height:8vh; width:8vw; position:absolute; bottom:2vh; left:2vw; ">
     <a href="http://www.darmarit.de">
       <img src="_static/darmarIT_logo_512.png">
     </a>
   </aside>

   
.. revealjs:: enjoy in scripting
   :data-transition: linear

   semantic path names and much more
   
   `fspath@GitHub <https://github.com/return42/fspath>`_

   .. rv_small::

      contributed by `return42 <http://github.com/return42>`_

   .. rv_note::

      After 10 years juggling with os.path, zipfile & Co. I thought it is time
      to bring back more *pythonic* to APIs. It is made with the philosophy that
      API's should be intuitive and their defaults should at least cover 80% of
      what programmer daily needs.  Started with the semantic file system
      pathes, it grows continuous and includes more and more handy stuff for the
      daily python scripting.


.. revealjs:: tired in os.path?
   :title-heading: h2

   are you tired in juggling with ...

   .. rv_code::

      parent_dir = os.path.abspath(
                       os.path.join(
                           os.path.dirname(__file__)
                           , os.path.pardir))

   and all that blody stuff? do you think this ..

   .. rv_code::

      parent_dir = FSPath(__file__).DIRNAME.ABSPATH / ".."


   is much readable .. than continue.


.. revealjs:: install
   :title-heading: h3

   users: works as usual

   .. rv_code::

      $ pip install [--user] fspath

   ... or a bleeding edge installation:

   .. rv_code::

      $ pip install --user git+http://github.com/return42/fspath.git

   
.. revealjs:: Verweise
   :title-heading: h2

   This slide show was build with the help of ..

   .. rv_small::

      - `sphinxjp.themes.revealjs <https://github.com/tell-k/sphinxjp.themes.revealjs>`_
      - `REVEAL.JS <http://lab.hakim.se/reveal-js>`_
      - `Sphinx-doc <http://www.sphinx-doc.org>`_
      - `reST <http://www.sphinx-doc.org/en/stable/rest.html>`_
      - `docutils <http://docutils.sourceforge.net/rst.html>`_
