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

      parent_dir = FSPath(__file__).DIRNAME.ABSPATH / '..'

   is much readable .. than continue.


.. revealjs:: install
   :title-heading: h2

   from `PyPI <https://pypi.python.org/pypi/fspath/>`_

   .. rv_code::
      :class: bash

      $ pip install [--user] fspath

   or a bleeding edge installation from `GitHub <http://github.com/return42/fspath.git>`_

   .. rv_code::
      :class: bash

      $ pip install --user git+http://github.com/return42/fspath.git


.. revealjs:: semantic path
   :title-heading: h3

   .. rv_code::
      :class: python

      >>> from fspath import FSPath
      >>> tmp = FSPath('~/tmp')
      >>> tmp
      '/home/user/tmp'
      >>> tmp.EXISTS
      False

   no additional import, no juggling with ``os.join(...)``

   simply slash ``/`` and ``foo.<method>`` calls
   
   .. rv_code::
      :class: python
              
      >>> [(tmp/x).makedirs() for x in ('foo', 'bar')]
      True, True
      >>> for n in tmp.listdir():
      ...     print(tmp / n)
      ... 
      /home/user/tmp/foo
      /home/user/tmp/bar


.. revealjs:: behaves as expected
   :title-heading: h3

   confused by  `'Changed in ..' <https://docs.python.org/3.5/library/os.html#os.makedirs>`_

   .. rv_code::
      :class: python

      >>> import os
      >>> os.makedirs(foo) &&
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/usr/lib/python3.5/os.py", line 241, in makedirs
        mkdir(name, mode)
        FileExistsError: [Errno 17] File exists:'/home/user/tmp/foo'

   aargh, creates intermediate but raise if exists?! 

   .. rv_code::
      :class: python

      >>> foo.makedirs()
      False

   FSPath behaves as expected :)


.. revealjs:: downloads & archives
   :title-heading: h3

   .. rv_code::
      :class: python

      >>> arch = foo / 'fspath.zip'
      >>> url = 'https://github.com/return42/fspath/archive/master.zip'

   ``FSPath.download`` -- super easy download + segmentation + nice ticker

   .. rv_code::
      :class: python

      >>> arch.download(url, chunkSize=1024, ticker=True)
      /home/user/tmp/foo/fspath.zip: [87.9 KB][===============    ]  83%

   ``FSPath.extract`` -- extract in one step, no matter ZIP or TAR 

   .. rv_code::
      :class: python

      >>> arch.ISTAR, arch.ISZIP
      (False, True)
      >>> arch.extract(foo)
      ['fspath-master/', 'fspath-master/.gitignore'
      , 'fspath-master/MAINFEST.in', 'fspath-master/Makefile'
      , 'fspath-master/README.rst',  ... ]

   .. rv_code::
      :class: python

      >>> folder = foo / 'fspath-master'

.. revealjs:: find files & strip
   :title-heading: h3

   ``glob`` -- shell like pattern in a single folder

   .. rv_code::
      :class: python

      >>> g_iter = folder.glob('*.py')
      >>> type(g_iter), len(list(g_iter))
      (<class 'generator'>, 1)

   ``relpath`` -- strip relative pathnames

   .. rv_code::
      :class: python

      >>> folder
      '/home/user/tmp/foo/fspath-master'
      >>> folder.relpath(tmp)
      'foo/fspath-master'
      
   ``reMatchFind`` -- recursive search files, matching regular expression
   
   .. rv_code::
      :class: python

      >>> py_iter = folder.reMatchFind(r'.*\.py$', relpath=True)
      >>> list(py_iter)
      ['setup.py', 'fspath/_which.py', 'fspath/win.py', ...]



.. revealjs:: more file & folder methods
   :title-heading: h3

   - ``.chdir`` --  change current working dir to *self*

   - ``.delete`` -- delete no matter if file or folder

   - ``.copyfile`` -- copy file (opt. with permission bits)

   - ``.copytree`` -- recursively copy the entire tree

   - ``.filesize`` -- Filesize in bytes or with precision

   .. rv_code::
      :class: python

      >>> arch.filesize()            # size in bytes (int)
      91502
      >>> arch.filesize(precision=3) # *human readable*
      '89.357 KB'


.. revealjs:: file & folder properties
   :title-heading: h3

   .. rv_code::
      :class: python

      >>> f = FSPath('../path/to/folder/filename.ext')

   .. rv_code::
      :class: python

      >>> f.DIRNAME
      '../path/to/folder'

   .. rv_code::
      :class: python

      >>> f.BASENAME
      'filename.ext'

   .. rv_code::
      :class: python

      >>> f.FILENAME
      'filename'

   .. rv_code::
      :class: python

      >>> f.SUFFIX
      '.ext'

   .. rv_code::
      :class: python

      >>> f.SKIPSUFFIX
      '../path/to/folder/filename'

.. revealjs:: file & folder properties
   :title-heading: h3

   .. rv_code::
      :class: python

      >>> f.ABSPATH
      '/share/fspath/local/path/to/folder/filename.ext'

   .. rv_code::
      :class: python

      >>> f.REALPATH
      '/share/fspath/path/to/folder/filename.ext'

   .. rv_code::
      :class: python

      >>> f.NTPATH
      '..\\path\\to\\folder\\filename.ext'

   .. rv_code::
      :class: python

      >>> f.POSIXPATH
      '../path/to/folder/filename.ext'

   .. rv_code::
      :class: python

      >>> home = FSPath("$HOME")
      >>> home
      '$HOME'
      >>> home.EXPANDVARS
      '/home/user'


      
.. revealjs:: file & folder properties
   :title-heading: h3

   - ``.EXISTS``      -- True if file/pathname exist
   - ``.SIZE``        -- Size in bytes
   - ``.READABLE``    -- True if file/path is readable  
   - ``.WRITEABLE``   -- True if file/path is writeable  
   - ``.EXECUTABLE``  -- True if file is executable
   - ``.ISDIR``       -- True if path is a folder  
   - ``.ISFILE``      -- True if path is a file  
   - ``.ISABSPATH``   -- True if path is absolute
   - ``.ISLINK``      -- True if path is a symbolic link  
   - ``.ISMOUNT``     -- True if path is a mountpoint

.. revealjs:: file & folder properties
   :title-heading: h3

   - ``.MTIME``       -- last modification time
   - ``.ATIME``       -- last access time
   - ``.CTIME``       -- last change time
   - ``.ISZIP``       -- True if path is a ZIP file
   - ``.ISTAR``       -- True if path is a TAR archive file









.. revealjs:: class methods

   .. rv_code::
      :class: python

      >>> FSPath.getHOME()
      '/home/user'

   .. rv_code::
      :class: python

      >>> FSPath.getCWD()
      '/share/fspath/local'



   
.. revealjs:: the FSPath type

   inheritance of ``unicode`` in Py2 and ``str`` in Py3

   .. rv_code::
      :class: python

      class FSPath(six.text_type):
           ...

   Take in mind, its a string type!

   .. rv_code::
      :class: python

      >>> [ (type(p), p) for p in tmp.splitpath()]
      [(<class 'fspath.fspath.FSPath'>, '/home/user')
        , (<class 'fspath.fspath.FSPath'>, 'tmp')]

   .. rv_code::
      :class: python

      >>> [ (type(p), p) for p in tmp.split('/')]
      [(<class 'str'>, ''), (<class 'str'>, 'home')
        , (<class 'str'>, 'user'), (<class 'str'>, 'tmp')]

           
.. revealjs:: the FSPath type

   constructor normalize without asking

   .. rv_code::
      :class: python

      >>> FSPath("foo") / ".." 
      '.'




      
.. revealjs:: call executables

   ``callEXE`` -- synchronous call and capture all in one

   .. rv_code::

      >>> from fspath import callEXE
      >>> out, err, rc = callEXE("arp", "-a")
      >>> print("stdout:\n%s" % out)
      stdout:
      dlan (192.168.1.122) at f4:06:8d:58:63:62 [ether] on wlp2s0
      storage (192.168.1.120) at 74:d4:35:b0:0b:ce [ether] on wlp2s0
      philips-tv (192.168.1.118) at b8:27:eb:83:a3:ab [ether] on wlp2s0

      >>> print("stderr: %s" % err)
      stderr: 
      >>> print("exit code = %d" % rc)
      exit code = 0


   
.. revealjs:: to be continued
   :title-heading: h3
   
   there is much more to show .. in the meantime take a look at the

   `API docs <https://return42.github.io/fspath/fspath-api/fspath.html>`_
      
.. revealjs::

   This slide show was build with the help of ..

   .. rv_small::

      - `sphinxjp.themes.revealjs <https://github.com/tell-k/sphinxjp.themes.revealjs>`_
      - `REVEAL.JS <http://lab.hakim.se/reveal-js>`_
      - `Sphinx-doc <http://www.sphinx-doc.org>`_
      - `reST <http://www.sphinx-doc.org/en/stable/rest.html>`_
      - `docutils <http://docutils.sourceforge.net/rst.html>`_
