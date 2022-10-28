import os

from setuptools import setup

version = open('VERSION', 'rb').read().decode('utf-8').strip()
long_description = open('README.md', 'rb').read().decode('utf-8')

setup(
    name='pytest-pycodestyle',
    version=version,
    description='pytest plugin to run pycodestyle',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/henry0312/pytest-pycodestyle',
    author='OMOTO Tsukasa',
    author_email='tsukasa@oomo.to',
    license='MIT',
    package_dir={'': 'src'},
    py_modules=['pytest_pycodestyle'],
    python_requires='~=3.7',
    install_requires=[
        'pytest>=7.0',
        'pycodestyle',
        'py',
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
