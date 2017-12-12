# pytest-codestyle

[![PyPI version](https://badge.fury.io/py/pytest-codestyle.svg)](https://badge.fury.io/py/pytest-codestyle)

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

## Licence

The MIT License  
Copyright (c) 2017 Tsukasa OMOTO

## Acknowledgments

- [pytest-dev / pytest-pep8 — Bitbucket](https://bitbucket.org/pytest-dev/pytest-pep8)
