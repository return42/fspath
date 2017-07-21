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
      :class: python

      parent_dir = os.path.abspath(
                       os.path.join(
                           os.path.dirname(__file__)
                           , os.path.pardir))

   and all that blody stuff? do you think this ..

   .. rv_code::
      :class: python

      parent_dir = FSPath(__file__).DIRNAME.ABSPATH / ".."


   is much readable .. than continue.


.. revealjs:: install
   :title-heading: h2

   from `PyPI <https://pypi.python.org/pypi/fspath/>`_

   .. rv_code::

      $ pip install [--user] fspath

   or a bleeding edge installation from `GitHub <http://github.com/return42/fspath.git>`_

   .. rv_code::

      $ pip install --user git+http://github.com/return42/fspath.git


.. revealjs:: semantic path
   :title-heading: h4

   .. rv_code::
      :class: python

      >>> from fspath import FSPath
      >>> tmp = FSPath('~/tmp')
      >>> tmp
      '/home/user/tmp'
      >>> tmp.EXISTS
      False

   no additional import / no ``os.join(...)`` / simply slash & ``foo.<method>``
   
   .. rv_code::
      :class: python

      >>> (tmp / 'foo').makedirs()
      True
      >>> (tmp / 'bar').makedirs()
      True
      >>> for n in tmp.listdir():
      ...     print(tmp / n)
      ... 
      /home/user/tmp/foo
      /home/user/tmp/bar


.. revealjs:: work as expected
   :title-heading: h4

   .. rv_code::
      :class: python

      >>> import os
      >>> os.makedirs(foo)
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/usr/lib/python3.5/os.py", line 241, in makedirs
        mkdir(name, mode)
        FileExistsError: [Errno 17] File exists:\
          '/home/user/tmp/foo'

   aargh, creates intermediate but raise if exists?!

   .. rv_code::
      :class: python

      >>> foo.makedirs()
      False

   FSPath behaves as expected :)

      
.. revealjs::

   This slide show was build with the help of ..

   .. rv_small::

      - `sphinxjp.themes.revealjs <https://github.com/tell-k/sphinxjp.themes.revealjs>`_
      - `REVEAL.JS <http://lab.hakim.se/reveal-js>`_
      - `Sphinx-doc <http://www.sphinx-doc.org>`_
      - `reST <http://www.sphinx-doc.org/en/stable/rest.html>`_
      - `docutils <http://docutils.sourceforge.net/rst.html>`_
