import fnmatch

import py.io
import pycodestyle
import pytest


def pytest_addoption(parser):
    group = parser.getgroup('codestyle')
    group.addoption('--codestyle', action='store_true',
                    default=False, help='run pycodestyle')


def pytest_configure(config):
    config.addinivalue_line('markers', 'codestyle: mark tests to be checked by pycodestyle.')


def pytest_collect_file(parent, path):
    config = parent.config
    if config.getoption('codestyle') and path.ext == '.py':
        # https://github.com/PyCQA/pycodestyle/blob/2.5.0/pycodestyle.py#L2295
        style_guide = pycodestyle.StyleGuide(paths=[str(path)], verbose=False)
        if not style_guide.excluded(filename=str(path)):
            options = style_guide.options
            return Item(path, parent, options)


class Item(pytest.Item, pytest.File):
    CACHE_KEY = 'codestyle/mtimes'

    def __init__(self, path, parent, options):
        super().__init__(path, parent)
        self.add_marker('codestyle')
        self.options = options
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
        checker = pycodestyle.Checker(filename=str(self.fspath),
                                      options=self.options)
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
