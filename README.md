LazyDictionary
==============

Lazily-evaluated dictionaries.

Overview
--------

    from lazydict import LazyDictionary
    lazy = LazyDictionary({'a': 1, 'b': 2})
    lazy['sum'] = lambda ld: ld['a'] + ld['b']
    print lazy['sum']
    # 3

A `LazyDicitonary` behaves mostly like an ordinary `dict`, except:

* item values are frozen upon reading, and

* values that are callable and take 1 or 0 arguments are called once before
  freezing

  * if the value takes 1 argument, the `LazyDictionary` instance will be
    supplied as the argument.

These features allow values in the dictionary to be dependent on other values in
the dictionary without regard to order of assignment.  It also allows lazily not
executing unused code:

    import tempfile
    lazy = LazyDictionary()
    lazy['temp'] = lambda: tempfile.mkdtemp()

If `lazy['temp']` is never an R-value, `mkdtemp()` will never be called.

Callable 1-argument values are nodes in directed graphs.  Edges are instances of
indexing the argument within the value's body.  In the first example, `sum` is
the root and `a` and `b` are leaves.  If a cycle exists in such a graph and a
node within the cycle is evaluated, a `CircularReferenceError` will be thrown
when the node is evaluated a second time.

If a frozen value is updated, a `ConstantRedefinitionError` will be thrown.


Install
-------

    pip install --pre LazyDictionary
