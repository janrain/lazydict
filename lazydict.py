from collections import MutableMapping
from threading import RLock
from inspect import getargspec
from copy import copy

def get_version():
    VERSION = (     # SEMANTIC
        1,          # major
        0,          # minor
        0,          # patch
        'beta.1',   # pre-release
        None        # build metadata
    )

    version = "%i.%i.%i" % (VERSION[0], VERSION[1], VERSION[2])
    if VERSION[3]:
        version += "-%s" % VERSION[3]
    if VERSION[4]:
        version += "+%s" % VERSION[4]
    return version

class LazyDictionaryError(Exception):
    pass

class CircularReferenceError(LazyDictionaryError):
    pass

class ConstantRedefinitionError(LazyDictionaryError):
    pass

class LazyDictionary(MutableMapping):
    def __init__(self, values={ }):
        self.lock = RLock()
        self.values = copy(values)
        self.states = {}
        for key in self.values:
            self.states[key] = 'defined'

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, key):
        with self.lock:
            if key in self.states:
                if self.states[key] == 'evaluating':
                    raise CircularReferenceError('value of "%s" depends on itself' % key)
                elif self.states[key] == 'defined':
                    value = self.values[key]
                    if callable(value):
                        (args, varargs, keywords, defaults) = getargspec(value)
                        if len(args) == 0:
                            self.states[key] = 'evaluating'
                            self.values[key] = value()
                        elif len(args) == 1:
                            self.states[key] = 'evaluating'
                            self.values[key] = value(self)
                    self.states[key] = 'evaluated'
            return self.values[key]

    def __contains__(self, key):
        return key in self.values

    def __setitem__(self, key, value):
        with self.lock:
            if key in self.states and self.states[key][0:4] == 'eval':
                raise ConstantRedefinitionError('"%s" is immutable' % key)
            self.values[key] = value
            self.states[key] = 'defined'

    def __delitem__(self, key):
        with self.lock:
            if key in self.states and self.states[key][0:4] == 'eval':
                raise ConstantRedefinitionError('"%s" is immutable' % key)
            del self.values[key]
            del self.states[key]
