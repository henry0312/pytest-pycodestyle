import fnmatch

import py.io
import pycodestyle
import pytest


def pytest_addoption(parser):
    group = parser.getgroup('codestyle')
    group.addoption('--codestyle', action='store_true',
                    default=False, help='run pycodestyle')

    parser.addini('codestyle_max_line_length', default=pycodestyle.MAX_LINE_LENGTH,
                  help='set maximum allowed line length (default: {max_line_length})'.format(
                      max_line_length=pycodestyle.MAX_LINE_LENGTH))
    parser.addini('codestyle_select', type='args',
                  help='select errors and warnings (default: [])')
    parser.addini('codestyle_ignore', type='args',
                  help='skip errors and warnings (default: [{ignored}])'.format(
                      ignored=pycodestyle.DEFAULT_IGNORE.replace(',', ' ')))
    parser.addini('codestyle_show_source', type="bool", default=True,
                  help='show source code for each error (default: True)')
    parser.addini('codestyle_exclude', type="args",
                  help='source files to be excluded from codestyle')


def pytest_configure(config):
    config.addinivalue_line('markers', 'codestyle: mark tests to be checked by pycodestyle.')


def pytest_collect_file(parent, path):
    config = parent.config
    if config.getoption('codestyle') and path.ext == '.py':
        if not any(path.fnmatch(pattern) for pattern in config.getini('codestyle_exclude')):
            return Item(path, parent)


class Item(pytest.Item, pytest.File):
    CACHE_KEY = 'codestyle/mtimes'

    def __init__(self, path, parent):
        super().__init__(path, parent)
        self.add_marker('codestyle')

        # https://github.com/pytest-dev/pytest/blob/92d6a0500b9f528a9adcd6bbcda46ebf9b6baf03/src/_pytest/nodes.py#L380
        # https://github.com/pytest-dev/pytest/blob/92d6a0500b9f528a9adcd6bbcda46ebf9b6baf03/src/_pytest/nodes.py#L101
        # https://github.com/moccu/pytest-isort/blob/44f345560a6125277f7432eaf26a3488c0d39177/pytest_isort.py#L142
        self._nodeid += '::CODESTYLE'

    def setup(self):
        if not hasattr(self.config, 'cache'):
            return

        old_mtime = self.config.cache.get(self.CACHE_KEY, {}).get(str(self.fspath), -1)
        mtime = self.fspath.mtime()
        if old_mtime == mtime:
            pytest.skip('previously passed pycodestyle checks')

    def runtest(self):
        # http://pycodestyle.pycqa.org/en/latest/api.html#pycodestyle.Checker
        # http://pycodestyle.pycqa.org/en/latest/advanced.html
        checker = pycodestyle.Checker(
                        filename=str(self.fspath),
                        max_line_length=int(self.config.getini('codestyle_max_line_length')),
                        select=self.config.getini('codestyle_select'),
                        ignore=self.config.getini('codestyle_ignore'),
                        show_source=self.config.getini('codestyle_show_source')
                    )
        file_errors, out, err = py.io.StdCapture.call(checker.check_all)
        if file_errors > 0:
            raise CodeStyleError(out)
        elif hasattr(self.config, 'cache'):
            # update cache
            # http://pythonhosted.org/pytest-cache/api.html
            cache = self.config.cache.get(self.CACHE_KEY, {})
            cache[str(self.fspath)] = self.fspath.mtime()
            self.config.cache.set(self.CACHE_KEY, cache)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(CodeStyleError):
            return excinfo.value.args[0]
        else:
            return super().repr_failure(excinfo)

    def reportinfo(self):
        # https://github.com/pytest-dev/pytest/blob/4678cbeb913385f00cc21b79662459a8c9fafa87/_pytest/main.py#L550
        # https://github.com/pytest-dev/pytest/blob/4678cbeb913385f00cc21b79662459a8c9fafa87/_pytest/doctest.py#L149
        return self.fspath, None, 'pycodestyle-check'


class CodeStyleError(Exception):
    """custom exception for error reporting."""
