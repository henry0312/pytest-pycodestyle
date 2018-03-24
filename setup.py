import os

from setuptools import setup

if os.environ.get('BUILD', None):
    packages = ['pytest-codestyle', 'pytest-pycodestyle']
else:
    packages = ['pytest-codestyle']

for name in packages:
    setup(
        name=name,
        version='1.1.2',
        description='pytest plugin to run pycodestyle',
        url='https://github.com/henry0312/pytest-codestyle',
        author='Tsukasa OMOTO',
        author_email='henry0312@gmail.com',
        license='MIT',
        py_modules=['pytest_codestyle'],
        python_requires='~=3.5',
        install_requires=[
            'pytest>=3.0,<4',
            'py>=1.5,<1.6',
            'pycodestyle>=2.3,<2.4',
        ],
        extras_require={
            'tests': ['tox'],
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
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
    )
