SHELL := /bin/bash
PYTHON ?= python
PACKAGE := pytest_pycodestyle              # hard‑code; one less subshell
VERSION := $(shell cat VERSION)

# ───────────────────────────── dev / test ──────────────────────────────
dev:            ## install package + test extras in editable mode
	$(PYTHON) -m pip install -e .[tests]

test:           ## run pytest suite
	pytest src tests

lint:           ## run style check (isort & pycodestyle) only
	pytest --collect-only -q >/dev/null  # ensure pytest is present
	pytest --isort --pycodestyle -q src tests

# ───────────────────────────── clean helpers ────────────────────────────
clean-build:    ## remove build artifacts
	rm -rf build dist
clean-pyc:      ## remove Python cache & egg‑info
	rm -rf {.,src,tests}/**/*.egg-info {.,src,tests}/.pytest_cache {.,src,tests}/__pycache__
clean: clean-build clean-pyc

# ───────────────────────────── packaging / publish ─────────────────────
deps-publish:   ## install build & twine
	$(PYTHON) -m pip install -e .[publish]

dist: clean-build deps-publish ## create sdist & wheel under dist/
	$(PYTHON) -m build

publish: dist   ## upload to PyPI (use TWINE_USERNAME/PASSWORD or .pypirc)
	twine upload --skip-existing dist/*

# ───────────────────────────── misc helpers ────────────────────────────
install:        ## pip‑install the package
	$(PYTHON) -m pip install .

uninstall:      ## pip‑uninstall the package
	$(PYTHON) -m pip uninstall -y $(PACKAGE)

update: clean uninstall install ## reinstall from a clean slate

# ───────────────────────────── meta ─────────────────────────────────────
.PHONY: dev test lint clean clean-build clean-pyc \
        deps-publish dist publish install uninstall update

