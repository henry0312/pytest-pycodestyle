# pytest-codestyle

[![PyPI version](https://badge.fury.io/py/pytest-codestyle.svg)](https://pypi.org/project/pytest-codestyle/)

[pytest](https://docs.pytest.org/en/latest/) plugin to run [pycodestyle](https://github.com/PyCQA/pycodestyle)

## Installation

```sh
pip install pytest-codestyle
```

## Usage

```sh
pytest --pycodestyle ...
```

For detail, please see `pytest -h` after installation.

## Configuration

The behavior can be configured in the same style of pycodestyle.  
(cf. [Configuration — pytest documentation](https://docs.pytest.org/en/latest/customize.html) and [Configuration — pycodestyle documentation](https://pycodestyle.readthedocs.io/en/latest/intro.html#configuration))

For example,

```
[pycodestyle]
max-line-length = 127

[tool:pytest]
addopts = --pycodestyle
```

## Licence

The MIT License  
Copyright (c) 2017 Tsukasa OMOTO

## Acknowledgments

- [pytest-dev / pytest-pep8 — Bitbucket](https://bitbucket.org/pytest-dev/pytest-pep8)
