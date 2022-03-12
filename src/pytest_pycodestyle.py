# https://docs.pytest.org/en/latest/writing_plugins.html
# https://docs.pytest.org/en/latest/example/nonpython.html#yaml-plugin

import optparse
import pathlib

import py.io
import pycodestyle
import pytest


def pytest_addoption(parser):
    group = parser.getgroup('pycodestyle')
    group.addoption('--pycodestyle', action='store_true',
                    default=False, help='run pycodestyle')


def pytest_configure(config):
    config.addinivalue_line('markers', 'pycodestyle: mark tests to be checked by pycodestyle.')


def pytest_collect_file(file_path: pathlib.Path, path, parent):
    """Create a Collector for the given path, or None if not relevant.

    See:
      - https://docs.pytest.org/en/7.0.x/reference/reference.html#pytest.hookspec.pytest_collect_file
    """
    config = parent.config
    if config.getoption('pycodestyle') and file_path.suffix == '.py':
        # https://github.com/PyCQA/pycodestyle/blob/2.5.0/pycodestyle.py#L2295
        style_guide = pycodestyle.StyleGuide(paths=[str(file_path)], verbose=False)
        if not style_guide.excluded(filename=str(file_path)):
            return File.from_parent(parent=parent, path=file_path, style_guide_options=style_guide.options)


class File(pytest.File):

    @classmethod
    def from_parent(cls, parent, path: pathlib.Path, style_guide_options: optparse.Values):
        # https://github.com/pytest-dev/pytest/blob/3e4c14bfaa046bcb5b75903470accf83d93f01ce/src/_pytest/nodes.py#L624
        _file = super().from_parent(parent=parent, path=path)
        # store options of pycodestyle
        _file.style_guide_options = style_guide_options
        return _file

    def collect(self):
        # https://github.com/pytest-dev/pytest/blob/3e4c14bfaa046bcb5b75903470accf83d93f01ce/src/_pytest/nodes.py#L524
        yield Item.from_parent(parent=self, name=self.name, nodeid=self.nodeid)


class Item(pytest.Item):
    CACHE_KEY = 'pycodestyle/mtimes'

    def __init__(self, name, parent, nodeid):
        # https://github.com/pytest-dev/pytest/blob/ee1950af7793624793ee297e5f48b49c8bdf2065/src/_pytest/nodes.py#L544
        super().__init__(name, parent=parent, nodeid=f"{nodeid}::PYCODESTYLE")
        self.add_marker('pycodestyle')
        # load options of pycodestyle
        self.options: optparse.Values = self.parent.style_guide_options

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
            raise PyCodeStyleError(out)
        elif hasattr(self.config, 'cache'):
            # update cache
            # http://pythonhosted.org/pytest-cache/api.html
            cache = self.config.cache.get(self.CACHE_KEY, {})
            cache[str(self.fspath)] = self.fspath.mtime()
            self.config.cache.set(self.CACHE_KEY, cache)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(PyCodeStyleError):
            return excinfo.value.args[0]
        else:
            return super().repr_failure(excinfo)

    def reportinfo(self):
        # https://github.com/pytest-dev/pytest/blob/4678cbeb913385f00cc21b79662459a8c9fafa87/_pytest/main.py#L550
        # https://github.com/pytest-dev/pytest/blob/4678cbeb913385f00cc21b79662459a8c9fafa87/_pytest/doctest.py#L149
        return self.fspath, None, 'pycodestyle-check'


class PyCodeStyleError(Exception):
    """custom exception for error reporting."""
