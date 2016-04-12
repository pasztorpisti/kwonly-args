# -*- coding: utf-8 -*-

import os
import re
import codecs
from setuptools import setup, find_packages


script_dir = os.path.dirname(os.path.abspath(__file__))


def find_version(*path):
    with codecs.open(os.path.join(script_dir, *path), 'r', 'utf8') as f:
        contents = f.read()

    # The version line must have the form
    # version_info = (X, Y, Z)
    m = re.search(
        r'^version_info\s*=\s*\(\s*(?P<v0>\d+)\s*,\s*(?P<v1>\d+)\s*,\s*(?P<v2>\d+)\s*\)\s*$',
        contents,
        re.MULTILINE,
    )
    if m:
        return '%s.%s.%s' % (m.group('v0'), m.group('v1'), m.group('v2'))
    raise RuntimeError('Unable to determine package version.')


with codecs.open(os.path.join(script_dir, 'README.rst'), 'r', 'utf8') as f:
    long_description = f.read()


setup(
    name='kwonly-args',
    version=find_version('src', 'kwonly_args', '__init__.py'),
    description='Python2 keyword-only argument emulation as a decorator. Python 3 compatible.',
    keywords='kwonly keyword only arguments args decorator',
    long_description=long_description,

    url='https://github.com/pasztorpisti/kwonly-args',

    author='István Pásztor',
    author_email='pasztorpisti@gmail.com',

    license='MIT',

    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages('src'),
    package_dir={'': 'src'},

    test_suite='tests',
    tests_require=['mock'],
)
