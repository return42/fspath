# -*- coding: utf-8 -*-
"""
    test_download
    ~~~~~~~~~~~~~

    Test FSPath.download method.

"""

from fspath import FSPath, OS_ENV

TEST_DOWNLOAD_URL="https://git.kernel.org/cgit/linux/kernel/git/stable/linux-stable.git/plain/COPYING"
MIN_FILESIZE=18000

def test():
    f = FSPath(OS_ENV.TEST_TEMPDIR) / "COPYING"
    if f.EXISTS:
        f.delete()
    assert not f.EXISTS
    f.download(TEST_DOWNLOAD_URL, chunkSize=1024, ticker=True)
    assert f.EXISTS
    assert f.SIZE > MIN_FILESIZE
