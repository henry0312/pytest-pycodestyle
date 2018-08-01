import os

from setuptools import setup

version = open('VERSION').read().strip()
long_description = open('README.md', 'rb').read().decode('utf-8')

setup(
    name='pytest-codestyle',
    version=version,
    description='pytest plugin to run pycodestyle',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/henry0312/pytest-codestyle',
    author='Tsukasa OMOTO',
    author_email='henry0312@gmail.com',
    license='MIT',
    py_modules=['pytest_codestyle'],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=[
        'pytest~=3.0',
        'py~=1.5',
        'pycodestyle~=2.3',
    ],
    extras_require={
        'tests': [
            'pytest-isort~=0.1',
        ],
    },
    # https://docs.pytest.org/en/latest/writing_plugins.html#making-your-plugin-installable-by-others
    entry_points={
        'pytest11': [
            'codestyle = pytest_codestyle',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Framework :: Pytest',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
