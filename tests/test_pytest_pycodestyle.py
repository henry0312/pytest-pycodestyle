import os

import pytest_pycodestyle

# https://docs.pytest.org/en/5.2.2/writing_plugins.html#testing-plugins
pytest_plugins = ["pytester"]


def test_option_false(testdir):
    p = testdir.makepyfile("""
        def test_option(request):
            flag = request.config.getoption('pycodestyle')
            assert flag is False
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_option_true(testdir):
    p = testdir.makepyfile("""
        def test_option(request):
            flag = request.config.getoption('pycodestyle')
            assert flag is True
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('--pycodestyle')
    result.assert_outcomes(passed=2)


def test_ini(testdir):
    testdir.makeini("""
        [pycodestyle]
        max-line-length = 80
        exclude = b.py
    """)
    testdir.tmpdir.ensure('a.py')
    testdir.tmpdir.ensure('b.py')  # to be skipped
    result = testdir.runpytest('--pycodestyle')
    result.assert_outcomes(passed=1)


def test_pytest_collect_file(testdir):
    testdir.tmpdir.ensure('a.py')
    testdir.tmpdir.ensure('b.py')
    testdir.tmpdir.ensure('c.txt')
    result = testdir.runpytest('--pycodestyle')
    result.assert_outcomes(passed=2)


def test_cache(testdir):
    testdir.tmpdir.ensure('a.py')
    # W292 no newline at end of file
    p = testdir.makepyfile("""
        def hello():
            print('hello')
    """)
    # first run
    result = testdir.runpytest('--pycodestyle')
    result.assert_outcomes(passed=1, failed=1)
    # second run
    result = testdir.runpytest('--pycodestyle')
    result.assert_outcomes(skipped=1, failed=1)


def test_no_cacheprovider(testdir):
    testdir.tmpdir.ensure('a.py')
    testdir.makepyfile("""
        def hello():
            print('hello')
    """)
    # first run
    result = testdir.runpytest('--pycodestyle', '-p', 'no:cacheprovider')
    result.assert_outcomes(passed=1, failed=1)
    # second run
    result = testdir.runpytest('--pycodestyle', '-p', 'no:cacheprovider')
    result.assert_outcomes(passed=1, failed=1)


def test_strict(testdir):
    p = testdir.makepyfile("""
        def test_blah():
            pass
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('--strict-markers', '--pycodestyle')
    result.assert_outcomes(passed=2)


def test_nodeid(testdir):
    p = testdir.makepyfile("""
        def test_nodeid():
            pass
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('-m', 'pycodestyle', '--pycodestyle', '-v')
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines(['test_nodeid.py::PYCODESTYLE PASSED *'])


class TestItem(object):

    def test_cache_key(self):
        assert pytest_pycodestyle.Item.CACHE_KEY == 'pycodestyle/mtimes'

    def test_init(self):
        pass

    def test_setup(self):
        pass

    def test_runtest(self):
        pass

    def test_repr_failure(self):
        pass

    def test_reportinfo(self):
        pass


class TestCodeStyleError(object):

    def test_subclass(self):
        assert issubclass(pytest_pycodestyle.PyCodeStyleError, Exception)
