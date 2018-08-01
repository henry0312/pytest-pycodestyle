# pytest-codestyle

[![PyPI version](https://badge.fury.io/py/pytest-codestyle.svg)](https://pypi.org/project/pytest-codestyle/)

[pytest](https://docs.pytest.org/en/latest/) plugin to run [pycodestyle](https://github.com/PyCQA/pycodestyle)

## Installation

```sh
pip install pytest-codestyle
```

## Usage

```sh
pytest --codestyle ...
```

For detail, please see `pytest -h` after installation.

## Configuration

You can configure options of pycodestyle with `setup.cfg` (or `pytest.ini`).  
(cf. [Configuration — pytest documentation](https://docs.pytest.org/en/latest/customize.html))

For example,

```
[tool:pytest]
codestyle_max_line_length = 100
codestyle_ignore = E302 E501
```

## Changelog

### 1.3.0 - Unreleased

- Support for Python 2.7 and 3.4.
  [fschulze (Florian Schulze)]


## Licence

The MIT License  
Copyright (c) 2017 Tsukasa OMOTO

## Acknowledgments

- [pytest-dev / pytest-pep8 — Bitbucket](https://bitbucket.org/pytest-dev/pytest-pep8)
