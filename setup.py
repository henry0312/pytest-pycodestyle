from setuptools import setup


setup(
    name='pytest-codestyle',
    version='1.1.0',
    description='pytest plugin to run pycodestyle',
    url='https://github.com/henry0312/pytest-codestyle',
    author='Tsukasa OMOTO',
    author_email='henry0312@gmail.com',
    license='MIT',
    py_modules=['pytest_codestyle'],
    python_requires='>=2.7,<3,>=3.6,<4',
    install_requires=[
        'pytest>=3.3,<3.4',
        'py>=1.5,<1.6',
        'pycodestyle>=2.3,<2.4',
    ],
    # https://docs.pytest.org/en/latest/writing_plugins.html#making-your-plugin-installable-by-others
    entry_points = {
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
    ],
)
