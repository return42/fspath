=================================================
fspath package
=================================================

.. raw:: html

    <aside id="logo" style="height:8vh; width:8vw; position:absolute; bottom:2vh; left:2vw; ">
     <a href="http://www.darmarit.de">
       <img src="_static/darmarIT_logo_512.png">
     </a>
   </aside>


.. revealjs:: fspath package
   :data-transition: linear
   :subtitle: enjoy in scripting
   :subtitle-heading: h4

   semantic path names and much more

   `return42/fspath@GitHub <https://github.com/return42/fspath>`_

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

   and all that bloody stuff? do you think this ..

   .. rv_code::
      :class: python

      parent_dir = FSPath(__file__).DIRNAME.ABSPATH / '..'

   is much more readable .. than continue.


.. revealjs:: install
   :title-heading: h2

   from `PyPI <https://pypi.python.org/pypi/fspath/>`_

   .. rv_code::
      :class: shell

      $ pip install [--user] fspath

   or a bleeding edge installation from `GitHub <http://github.com/return42/fspath.git>`_

   .. rv_code::
      :class: shell

      $ pip install --user git+http://github.com/return42/fspath.git

.. revealjs:: Content
   :title-heading: h2

   - `semantic path <#/4>`_
   - `be expressive in daily use cases <#/7>`_ 
   - `file name suffix explained <#/15>`_ 
   - `the FSPath type <#/20>`_
   - `OS_ENV <#/22>`_
   - `Command Line Interface <#/24>`_
   - `versioning scheme <#/31>`_

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

   confused by ``makedirs`` `'Changed in ..' <https://docs.python.org/3.5/library/os.html#os.makedirs>`_?

   .. rv_code::
      :class: python

      >>> foo = tmp / 'foo'
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


.. revealjs:: return of dispersed operations
   :title-heading: h3

   tired in meaningless ``foo``, ``foo2`` and ``fooN`` functions?

   .. rv_code::
      :class: python

      def copyfile(self, dest, preserve=False):
         if preserve:
            shutil.copy2(self, dest)
         else:
            shutil.copy(self, dest)

   you think *delete* means **delete!**

   .. rv_code::
      :class: python

      def delete(self):
          if self.ISDIR:
              self.rmtree()
          else:
              os.remove(self)

.. revealjs:: be expressive in daily use cases
   :title-heading: h3

   just read my entire text file

   .. rv_code::
      :class: python

      readme = FSPath('README.txt').readFile()

   open a path name with its associated desktop application

   .. rv_code::
      :class: python

      >>> FSPath('index.html').startFile() # opens HTML-browser showing
      >>>

   .. rv_code::
      :class: python

      >>> FSPath('.').startFile()          # opens file-explorer at CWD

   .. rv_small::

      M$-Win has nativ support in Python. On Darwin and FreeBSD the `open
      <https://www.freebsd.org/cgi/man.cgi?open>`__ command is used. On other OS
      (e.g. Linux) the `xdg-open
      <https://portland.freedesktop.org/doc/xdg-open.html>`_ is used.


.. revealjs:: be expressive in daily use cases
   :title-heading: h3

   ``FSPath`` gives us prototypes with meaningful defaults

   .. rv_code::
      :class: python

      def openTextFile(self
                       , mode='rt', encoding='utf-8'
                       , errors='strict', buffering=1
                       , newline=None):

   and without meaningless arguments

   .. rv_code::
      :class: python

      def openBinaryFile(self
                         , mode='rb', errors='strict'
                         , buffering=None):

   if you have time, compare this with `open
   <https://docs.python.org/3.5/library/functions.html#open>`__


.. revealjs:: be expressive in daily use cases
   :title-heading: h3

   just download and extract

   .. rv_code::
      :class: python

      >>> arch = foo / 'fspath.zip'
      >>> url = 'https://github.com/return42/fspath/archive/master.zip'

   ``.download`` -- super easy download + segmentation + ticker

   .. rv_code::
      :class: python

      >>> arch.download(url, chunkSize=1024, ticker=True)
      /home/user/tmp/foo/fspath.zip: [87.9 KB][==============    ]  83%

   ``.extract`` -- extract in one step, no matter ZIP or TAR

   .. rv_code::
      :class: python

      >>> arch.ISTAR, arch.ISZIP
      (False, True)
      >>> arch.extract(foo)
      ['fspath-master/', 'fspath-master/.gitignore' ...


.. revealjs:: be expressive in daily use cases
   :title-heading: h3

   ``.glob`` -- shell like pattern in a single folder

   .. rv_code::
      :class: python

      >>> folder = foo / 'fspath-master'
      >>> g_iter = folder.glob('*.py')
      >>> type(g_iter), len(list(g_iter))
      (<class 'generator'>, 1)

   ``.reMatchFind`` -- search files recursively by `regexp <https://docs.python.org/library/re.html>`_

   .. rv_code::
      :class: python

      >>> rst_files = folder.reMatchFind(r'.*\.rst$')

   example: change suffix of all '.rst' files in your tree

   .. rv_code::
      :class: python

      >>> moved_files = [f.move(f.suffix('.txt')) for f in rst_files]


.. revealjs:: be expressive in daily use cases
   :title-heading: h3

   ``.relpath`` -- strip relative pathnames

   .. rv_code::
      :class: python

      >>> folder
      '/home/user/tmp/foo/fspath-master'
      >>> folder.relpath(tmp)
      'foo/fspath-master'

   .. rv_code::
      :class: python

      >>> py_iter = folder.reMatchFind(r'.*\.py$', relpath=True)
      >>> list(py_iter)
      ['setup.py', 'fspath/_which.py', 'fspath/win.py', ...]

   ``.filesize`` -- (human) readable file size

   .. rv_code::
      :class: python

      >>> arch.filesize()            # size in bytes (int)
      91502
      >>> arch.filesize(precision=3) # switch to human readable output
      '89.357 KB'
      >>> foo.filesize(precision=0)  # switch to human readable output
      '12 MB'


.. revealjs:: be expressive in daily use cases
   :title-heading: h3

   run executable without any rocket since

   .. rv_code::
      :class: python

      >>> proc = FSPath('arp').Popen('-a',)
      >>> stdout, stderr = proc.communicate()
      >>> retVal = proc.returncode

   ``callEXE`` -- synchronous call and capture all in one

   .. rv_code::
      :class: python

      >>> from fspath import callEXE
      >>> out, err, rc = callEXE('arp', '-a', '192.168.1.120')
      >>> print("out:'%s...' | err='%s' | exit code=%d"
                % (out[:24], err, rc))
      out:'storage (192.168.1.120) ...' | err='' | exit code=0

   .. rv_code::
      :class: python

      >>> callEXE('arp', '-a', 'xyz')
      ('', 'xyz: Unknown host\n', 255)

.. revealjs:: more file & folder methods
   :title-heading: h3

   - ``.chdir`` --  change current working dir to *self*

   - ``.walk`` -- generate filenames of tree (see `os.walk <https://docs.python.org/3/library/os.html#os.walk>`_)

   - ``.delete`` -- delete! .. no matter if file or folder

   - ``.copyfile`` -- copy file (opt. with permission bits)

   - ``.copytree`` -- recursively copy the entire tree

   - ``.filesize`` -- Filesize in bytes or with precision

   - ``.suffix`` -- return path name with *new* suffix

.. revealjs:: common class members

   To be complete with path names.

   .. rv_code::
      :class: python

      >>> FSPath.getHOME()
      '/home/user'

   .. rv_code::
      :class: python

      >>> FSPath.getCWD()
      '/share/fspath/local'

   ``FSPath.OS`` -- shortcut to common OS properties

   .. rv_code::
      :class: python

      >>> pprint(FSPath.OS)
      {'altsep'   : None       ,  'curdir'   : '.'  ,
       'extsep'   : '.'        ,  'linesep'  : '\n' ,
       'pathsep'  : ':'        ,  'sep'      : '/'  ,
       'devnull'  : '/dev/null',  'defpath'  : ':/bin:/usr/bin'
       }


.. revealjs:: file name suffix explained
   :title-heading: h3

   .. rv_code::
      :class: python

      >>> filename = FSPath('../path/to/folder/filename.ext')

   *dot* is a part of the *suffix*

   .. rv_code::
      :class: python

      >>> filename.SUFFIX
      '.ext'

   change suffix *in place*

   .. rv_code::
      :class: python

      >>> filename.suffix('.rst')
      '../path/to/folder/filename.rst'

   or even throw it away

   .. rv_code::
      :class: python

      >>> filename.SKIPSUFFIX
      '../path/to/folder/filename'


.. revealjs:: more file & folder properties
   :title-heading: h3

   .. rv_code::
      :class: python

      >>> filename.DIRNAME
      '../path/to/folder'

   .. rv_code::
      :class: python

      >>> filename.BASENAME
      'filename.ext'

   .. rv_code::
      :class: python

      >>> filename.FILENAME
      'filename'

   .. rv_code::
      :class: python

      >>> filename.ABSPATH
      '/share/fspath/local/path/to/folder/filename.ext'

   .. rv_code::
      :class: python

      >>> filename.REALPATH
      '/share/fspath/path/to/folder/filename.ext'



.. revealjs:: more file & folder properties
   :title-heading: h3

   .. rv_code::
      :class: python

      >>> filename.NTPATH
      '..\\path\\to\\folder\\filename.ext'

   .. rv_code::
      :class: python

      >>> filename.POSIXPATH
      '../path/to/folder/filename.ext'

   known from shell

   .. rv_code::
      :class: python

      >>> home = FSPath("$HOME")
      >>> home
      '$HOME'
      >>> home.EXPANDVARS
      '/home/user'

   .. rv_code::
      :class: python

      >>> home = FSPath("~/tmp")
      >>> home.EXPANDUSERS
      '/home/user'


.. revealjs:: more file & folder properties
   :title-heading: h3

   - ``.EXISTS``      -- True if file/path name exist
   - ``.SIZE``        -- Size in bytes
   - ``.READABLE``    -- True if file/path is readable
   - ``.WRITEABLE``   -- True if file/path is writeable
   - ``.EXECUTABLE``  -- True if file is executable
   - ``.ISDIR``       -- True if path is a folder
   - ``.ISFILE``      -- True if path is a file
   - ``.ISABSPATH``   -- True if path is absolute
   - ``.ISLINK``      -- True if path is a symbolic link
   - ``.ISMOUNT``     -- True if path is a mountpoint


.. revealjs:: more file & folder properties
   :title-heading: h3

   - ``.MTIME``       -- last modification time
   - ``.ATIME``       -- last access time
   - ``.CTIME``       -- last change time
   - ``.ISZIP``       -- True if path is a ZIP file
   - ``.ISTAR``       -- True if path is a TAR archive file


.. revealjs:: the FSPath type

   inheritance of ``unicode`` in Py2 and ``str`` in Py3

   .. rv_code::
      :class: python

      class FSPath(six.text_type):
           ...

   constructor normalize without asking

   .. rv_code::
      :class: python

      >>> FSPath('goes/up/../and/../down')
      'goes/down'

   works with anyone who accept strings

   .. rv_code::
      :class: python

      >>> os.stat(FSPath.getHOME())
      os.stat_result(st_mode=16877, st_ino=1966082, ...


.. revealjs:: the FSPath type
   :title-heading: h3
   :subtitle: Take in mind, its a string type!
   :subtitle-heading: h4

   ``FSPath`` member call returns FSPath instances

   .. rv_code::
      :class: python

      >>> type(folder.splitpath()[-1])
      <class 'fspath.fspath.FSPath'>

   call of inherited string member returns string types

   .. rv_code::
      :class: python

      >>> type(folder.split(home.OS.sep)[-1])
      <class 'str'>


.. revealjs:: OS_ENV
   :title-heading: h3
   :subtitle: a singleton for the environment
   :subtitle-heading: h4

   environment variables are attributes

   .. rv_code::
      :class: python

      >>> from fspath import OS_ENV
      >>> OS_ENV.SHELL
      '/bin/bash'

   you can get or set

   .. rv_code::
      :class: python

      >>> OS_ENV.TMP = '/tmp/xyz'
      >>> FSPath('$TMP').EXPANDVARS
      '/tmp/xyz'

.. revealjs:: OS_ENV
   :title-heading: h3

   unknown environment request raises ``KeyError``

   .. rv_code::
      :class: python

      >>> OS_ENV.XYZ
      Traceback (most recent call last):
      ...
      KeyError: 'XYZ'

   use ``.get`` to avoid exceptions

   .. rv_code::
      :class: python

      >>> OS_ENV.get('XYZ', 'not defined')
      'not defined'
      >>> OS_ENV.get('XYZ')
      >>>

.. revealjs:: Command Line Interface
   :title-heading: h3
   :subtitle: a CLI with a pinch of sugar
   :subtitle-heading: h4

   .. rv_code::
      :class: python

      # -*- coding: utf-8; mode: python -*-
      # file: foobar/main.py

      """foobar CLI"""

      import sys
      from fspath import CLI

      def main():
          cli = CLI(description=__doc__)
          # define CLI
          ...
          # run CLI
          cli()


.. revealjs:: CLI & setup
   :title-heading: h3

   in projects ``setup.py`` add entry point for ``main()``

   .. rv_code::
      :class: python

      setup(name = "foobar"
            ...
            , entry_points = {
                'console_scripts': [
                    'foobar = foobar.main:main' ]}
            ...
            )

.. revealjs:: CLI's subcommands
   :title-heading: h3

   implement a ``cli`` wrapper for each subcommand

   .. rv_code::
      :class: python

      def cli_hello(cliArgs):
          """another 'hello world'"""
          print('hello world')

   ``cliArgs.folder`` we will be of type ``FSPath``

   .. rv_code::
      :class: python
      
      def cli_listdir(cliArgs):
          """list directory"""
          for f in cliArgs.folder.listdir():
              l = f.upper() if cliArgs.upper else f
              f = cliArgs.folder / f
              if cliArgs.verbose:
                  l = '[%10s] ' % (f.filesize(precision=0)) + l  
              print(l, end = ('\n' if cliArgs.verbose else ', '))

.. revealjs:: CLI's subcommands
   :title-heading: h3

   `CLI <https://github.com/return42/fspath/blob/master/fspath/cli.py>`__ is an
   `argparse <https://docs.python.org/3.5/library/argparse.html>`_
   implementation.

   .. rv_code::
      :class: python

      def main():
          ...
          # define CLI
          hello   = cli.addCMDParser(cli_hello, cmdName='hello')
          listdir = cli.addCMDParser(cli_listdir, cmdName='dir')
          listdir.add_argument("folder", type = FSPath
                               , nargs = "?", default = FSPath(".")
                               , help = "path of the folder")
          listdir.add_argument("--upper", action = 'store_true'
                               , help = "convert to upper letters")

   using ``type=FSPath`` for file and path name arguments gives us the power of
   ``FSPath`` (see ``cli_listdir(...)``)
                               
.. revealjs:: CLI usage
   :title-heading: h3

   the *over all* help

   .. rv_code::
      :class: shell

      $ foobar --help
      usage: foobar [-h] [--debug] [--verbose] [--quiet] \
                    {hello, dir} ...

      optional arguments:
        -h, --help  show this help message and exit
        --debug     run in debug mode (default: False)
        --verbose   run in verbose mode (default: False)
        --quiet     run in quiet mode (default: False)

      commands:
        {hello,dir}
          hello      another 'hello world'
          dir        list directory

.. revealjs:: CLI subcommands usage
   :title-heading: h3

   the *subcommand* ``--help``

   .. rv_code::
      :class: shell

      $ foobar dir --help

      usage: foobar dir [-h] [--upper] [folder]

      positional arguments:
        folder      path of the folder (default: .)

      optional arguments:
        -h, --help  show this help message and exit
        --upper     convert to upper letters (default: False)

      list directory

.. revealjs:: show how it works
   :title-heading: h3

   run subcommand ``dir``

   .. rv_code::
      :class: shell

      $ foobar dir /
      initrd.img.old, initrd.img, var, vmlinuz, home ...
   
   and with global option ``verbose`` 

   .. rv_code::
      :class: shell

      $ foobar.py --verbose dir /    
      [     40 MB] initrd.img.old
      [     40 MB] initrd.img
      [      4 KB] var
      [      7 MB] vmlinuz
      [      4 KB] home
      ...

.. revealjs:: versioning scheme
   :title-heading: h3

   As long as every new release is fully downward compatible a `serial
   versioning
   <https://packaging.python.org/tutorials/distributing-packages/#serial-versioning>`_
   is enough.

   Version numbers follow scheme

   ``YYYYMMDD``


.. revealjs:: to be continued
   :title-heading: h3

   there is much more to show .. in the meantime take a look at the

   `API docs <https://return42.github.io/fspath/fspath-api/fspath.html>`_


.. revealjs::

   This slide show was build with the help of ..

   .. rv_small::

      - `sphinxjp.themes.revealjs <https://github.com/return42/sphinxjp.themes.revealjs>`_
      - `REVEAL.JS <http://lab.hakim.se/reveal-js>`_
      - `Sphinx-doc <http://www.sphinx-doc.org>`_
      - `reST <http://www.sphinx-doc.org/en/stable/rest.html>`_
      - `docutils <http://docutils.sourceforge.net/rst.html>`_
