# pytest-pycodestyle

[![PyPI version](https://badge.fury.io/py/pytest-pycodestyle.svg)](https://pypi.org/project/pytest-pycodestyle/)

[pytest](https://docs.pytest.org/en/latest/) plugin to run [pycodestyle](https://github.com/PyCQA/pycodestyle)

## Installation

```sh
pip install pytest-pycodestyle
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
Copyright (c) 2019 OMOTO Tsukasa

## Acknowledgments

- [pytest-dev / pytest-pep8 — Bitbucket](https://bitbucket.org/pytest-dev/pytest-pep8)
