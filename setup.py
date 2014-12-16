#!/usr/bin/env python
"""
Lazily-evaluated dictionaries

A ``LazyDicitonary`` behaves mostly like an ordinary ``dict``, except:

* item values are frozen upon reading, and

* values that are callable and take 1 or 0 arguments are called once before
  freezing

  * if the value takes 1 argument, the ``LazyDictionary`` instance will be
    supplied as the argument.
"""

from setuptools import setup

from lazydict import get_version

doc = __doc__.strip("\n").split("\n")

classifiers = """
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: OS Independent
"""

setup(
    name=            'LazyDictionary',
    version=         get_version(),
    url=             'https://github.com/janrain/lazydict',
    download_url=    'https://pypi.python.org/packages/source/L/LazyDictionary/LazyDictionary-{}.tar.gz'.format(get_version()),
    author=          "Colin von Heuring",
    author_email=    "colin@von.heuri.ng",
    description=     doc[0],
    long_description="\n".join(doc[2:]),
    classifiers=     filter(None, classifiers.split("\n")),
    license=         "MIT License",
    platforms=       ['any'],
    py_modules=      ['lazydict'],
    test_suite=      'test'
)
