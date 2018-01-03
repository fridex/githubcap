#!/usr/bin/python3

import sys
import os
from setuptools import setup, find_packages


if sys.version_info[0] != 3:
    sys.exit("Python3 is required in order to install githubcap")


def get_requirements():
    with open('requirements.txt') as fd:
        return fd.read().splitlines()


def get_version():
    with open(os.path.join('githubcap', '__init__.py')) as f:
        content = f.readline()

    for line in content:
        if line.startswith('__version__ ='):
            # dirty, remove trailing and leading chars
            return line.split(' = ')[1][1:-2]


def get_long_description():
    with open('README.rst', 'r') as f:
        return f.read()


setup(
    name='githubcap',
    version=get_version(),
    entry_points={
        'console_scripts': ['githubcap-cli=githubcap.cli:cli']
    },
    packages=find_packages(),
    install_requires=get_requirements(),
    author='Fridolin Pokorny',
    author_email='fridolin.pokorny@gmail.com',
    maintainer='Fridolin Pokorny',
    maintainer_email='fridolin.pokorny@gmail.com',
    description='Tool and library for interacting with GitHub API v3',
    long_description=get_long_description(),
    url='https://github.com/fridex/githubcap',
    license='ASL v2.0',
    keywords='github tool api',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ]
)
