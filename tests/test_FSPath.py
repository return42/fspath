# -*- coding: utf-8; mode: python -*-
"""test FSPath"""

import uuid
from fspath import FSPath, OS_ENV

TEST_DOWNLOAD_URL="https://git.kernel.org/cgit/linux/kernel/git/stable/linux-stable.git/plain/COPYING"
MIN_FILESIZE=18000

TMP = FSPath(OS_ENV.TEST_TEMPDIR)

def test_download():
    url = 'https://github.com/return42/fspath/archive/master.zip'
    arch = TMP / 'fspath.zip'

    if arch.EXISTS:
        arch.delete()
    assert not arch.EXISTS

    arch.download(url,
                  chunksize=1024, ticker=True)
    assert arch.EXISTS
    assert arch.SIZE > MIN_FILESIZE

def test_ZIP():
    arch = TMP / 'fspath.zip'
    arch_folder = TMP / 'fspath-master'
    if arch_folder.EXISTS:
        arch_folder.delete()
    assert not arch.ISTAR
    assert arch.ISZIP
    arch.extract(TMP)
    assert arch_folder.EXISTS

def test_makedirs():
    foo = TMP / 'foo'
    if foo.EXISTS:
        foo.delete()
    assert foo.makedirs()
    assert not foo.makedirs()
    
