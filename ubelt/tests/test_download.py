import ubelt as ub
import pytest
from os.path import basename, join, exists


@pytest.mark.timeout(5)
def test_download_no_fpath():
    url = 'http://i.imgur.com/rqwaDag.png'

    dpath = ub.ensure_app_cache_dir('ubelt')
    fname = basename(url)
    fpath = join(dpath, fname)

    ub.delete(fpath)
    assert not exists(fpath)

    got_fpath = ub.download(url)

    assert got_fpath == fpath
    assert exists(fpath)


@pytest.mark.timeout(5)
def test_download_with_fpath():
    url = 'http://i.imgur.com/rqwaDag.png'

    dpath = ub.ensure_app_cache_dir('ubelt', 'tests')
    fname = basename(url)
    fpath = join(dpath, fname)

    ub.delete(fpath)
    assert not exists(fpath)

    got_fpath = ub.download(url, fpath=fpath)
    assert got_fpath == fpath
    assert exists(fpath)

    with open(got_fpath, 'rb') as file:
        data = file.read()
    assert len(data) > 1200, 'should have downloaded some bytes'


@pytest.mark.timeout(5)
def test_download_chunksize():
    # url = 'https://www.dropbox.com/s/jl506apezj42zjz/ibeis-win32-setup-ymd_hm-2015-08-01_16-28.exe?dl=1'
    url = 'http://i.imgur.com/rqwaDag.png'

    dpath = ub.ensure_app_cache_dir('ubelt')
    fname = basename(url)
    fpath = join(dpath, fname)

    ub.delete(fpath)
    assert not exists(fpath)

    got_fpath = ub.download(url, chunksize=2)

    assert got_fpath == fpath
    assert exists(fpath)


@pytest.mark.timeout(5)
def test_grabdata_cache():
    """
    Check where the url is downloaded to when fpath is not specified.
    """
    url = 'http://i.imgur.com/rqwaDag.png'

    dpath = ub.ensure_app_cache_dir('ubelt')
    fname = basename(url)
    fpath = join(dpath, fname)

    got_fpath = ub.grabdata(url)
    assert got_fpath == fpath
    assert exists(fpath)

    ub.delete(fpath)
    assert not exists(fpath)

    ub.grabdata(url)
    assert exists(fpath)


@pytest.mark.timeout(5)
def test_grabdata_url_only():
    """
    Check where the url is downloaded to when fpath is not specified.
    """
    url = 'http://i.imgur.com/rqwaDag.png'

    dpath = ub.ensure_app_cache_dir('ubelt')
    fname = basename(url)
    fpath = join(dpath, fname)

    got_fpath = ub.grabdata(url)
    assert got_fpath == fpath
    assert exists(fpath)


@pytest.mark.timeout(5)
def test_grabdata_with_fpath():
    """
    Check where the url is downloaded to when fpath is not specified.
    """
    url = 'http://i.imgur.com/rqwaDag.png'

    dpath = ub.ensure_app_cache_dir('ubelt')
    fname = basename(url)
    fpath = join(dpath, fname)

    got_fpath = ub.grabdata(url, fpath=fpath, verbose=3)
    assert got_fpath == fpath
    assert exists(fpath)

    ub.delete(fpath)
    assert not exists(fpath)

    ub.grabdata(url, fpath=fpath, verbose=3)
    assert exists(fpath)


def test_grabdata_value_error():
    """
    Check where the url is downloaded to when fpath is not specified.
    """
    url = 'http://i.imgur.com/rqwaDag.png'

    dpath = ub.ensure_app_cache_dir('ubelt')
    fname = basename(url)
    fpath = join(dpath, fname)

    with pytest.raises(ValueError):
        ub.grabdata(url, fname=fname, fpath=fpath, dpath=dpath)

    with pytest.raises(ValueError):
        ub.grabdata(url, fname=fname, fpath=fpath)

    with pytest.raises(ValueError):
        ub.grabdata(url, dpath=dpath, fpath=fpath)

    with pytest.raises(ValueError):
        ub.grabdata(url, fpath=fpath, appname='foobar')

    with pytest.raises(ValueError):
        ub.grabdata(url, dpath=dpath, appname='foobar')


@pytest.mark.timeout(5)
def test_download_bad_url():
    """
    Check that we error when the url is bad

    CommandLine:
        python -m ubelt.tests.test_download test_download_bad_url --verbose
    """
    url = 'http://a-very-incorrect-url'

    dpath = ub.ensure_app_cache_dir('ubelt', 'tests')
    fname = basename(url)
    fpath = join(dpath, fname)

    ub.delete(fpath)
    assert not exists(fpath)

    from ubelt.util_download import URLError
    with pytest.raises(URLError):
        ub.download(url, fpath=fpath, verbose=1)


@pytest.mark.timeout(5)
def test_grabdata_fname_only():
    url = 'http://i.imgur.com/rqwaDag.png'

    dpath = ub.ensure_app_cache_dir('ubelt')
    fname = 'mario.png'
    fpath = join(dpath, fname)

    got_fpath = ub.grabdata(url, fname=fname)
    assert got_fpath == fpath
    assert exists(fpath)


@pytest.mark.timeout(5)
def test_grabdata_dpath_only():
    url = 'http://i.imgur.com/rqwaDag.png'

    dpath = ub.ensure_app_cache_dir('ubelt', 'test')
    fname = basename(url)
    fpath = join(dpath, fname)

    got_fpath = ub.grabdata(url, dpath=dpath)
    assert got_fpath == fpath
    assert exists(fpath)


@pytest.mark.timeout(5)
def test_grabdata_fpath_and_dpath():
    url = 'http://i.imgur.com/rqwaDag.png'
    with pytest.raises(ValueError):
        ub.grabdata(url, fpath='foo', dpath='bar')


if __name__ == '__main__':
    r"""
    CommandLine:
        pytest ubelt/tests/test_download.py
    """
    import xdoctest
    xdoctest.doctest_module(__file__)
