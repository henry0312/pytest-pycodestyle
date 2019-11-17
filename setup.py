import os

from setuptools import setup

version = open('VERSION', 'rb').read().decode('utf-8').strip()
long_description = open('README.md', 'rb').read().decode('utf-8')

setup(
    name='pytest-codestyle',
    version=version,
    description='pytest plugin to run pycodestyle',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/henry0312/pytest-codestyle',
    author='OMOTO Tsukasa',
    author_email='tsukasa@oomo.to',
    license='MIT',
    py_modules=['pytest_codestyle'],
    python_requires='~=3.5',
    install_requires=[
        'pytest',
        'pycodestyle',
    ],
    extras_require={
        'tests': [
            'pytest-isort',
        ],
    },
    # https://docs.pytest.org/en/latest/writing_plugins.html#making-your-plugin-installable-by-others
    entry_points={
        'pytest11': [
            'pycodestyle = pytest_pycodestyle',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Framework :: Pytest',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
