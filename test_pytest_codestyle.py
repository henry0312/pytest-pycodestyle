import os

import pytest_codestyle

# https://docs.pytest.org/en/latest/writing_plugins.html#testing-plugins
pytest_plugins = ["pytester"]


def test_option_false(testdir):
    p = testdir.makepyfile("""
        def test_option(request):
            flag = request.config.getoption('codestyle')
            assert flag is False
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_option_true(testdir):
    p = testdir.makepyfile("""
        def test_option(request):
            flag = request.config.getoption('codestyle')
            assert flag is True
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('--codestyle')
    result.assert_outcomes(passed=2)


def test_ini(testdir):
    testdir.makeini("""
        [pytest]
        codestyle_max_line_length = 80
        codestyle_select = a b c
        codestyle_ignore = d e f
        codestyle_exclude = exclude.py path/to/another/exclude.py
    """)
    p = testdir.makepyfile("""
        def test_ini(request):
            config = request.config
            max_line_length = '80'
            assert config.getini('codestyle_max_line_length') == max_line_length
            select = ['a', 'b', 'c']
            assert config.getini('codestyle_select') == select
            ignore = ['d', 'e', 'f']
            assert config.getini('codestyle_ignore') == ignore
            assert config.getini('codestyle_show_source') is True
            exclude = ['{dirname}/{base}/exclude.py', '{dirname}/{base}/path/to/another/exclude.py']
            assert config.getini('codestyle_exclude') == exclude
    """.format(dirname=testdir.tmpdir.dirname, base=testdir.tmpdir.basename))
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('--codestyle')
    result.assert_outcomes(passed=2)


def test_pytest_collect_file(testdir):
    testdir.tmpdir.ensure('a.py')
    testdir.tmpdir.ensure('b.py')
    testdir.tmpdir.ensure('c.txt')
    result = testdir.runpytest('--codestyle')
    result.assert_outcomes(passed=2)


def test_pytest_collect_file_with_exclude(testdir):
    testdir.makeini("""
        [pytest]
        codestyle_exclude = a.py path/to/c.py
    """)
    testdir.tmpdir.ensure('a.py')
    testdir.tmpdir.ensure('b.py')
    testdir.tmpdir.ensure('path/to/c.py')
    result = testdir.runpytest('--codestyle')
    result.assert_outcomes(passed=1)


def test_cache(testdir):
    testdir.tmpdir.ensure('a.py')
    # W292 no newline at end of file
    p = testdir.makepyfile("""
        def hello():
            print('hello')
    """)
    # first run
    result = testdir.runpytest('--codestyle')
    result.assert_outcomes(passed=1, failed=1)
    # second run
    result = testdir.runpytest('--codestyle')
    result.assert_outcomes(skipped=1, failed=1)


class TestItem(object):

    def test_cache_key(self):
        assert pytest_codestyle.Item.CACHE_KEY == 'codestyle/mtimes'

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
        assert issubclass(pytest_codestyle.CodeStyleError, Exception)
