from unittest import TestCase
from lazydict import LazyDictionary, CircularReferenceError, \
                     ConstantRedefinitionError

class TestLazyDictionary(TestCase):

    def test_circular_reference_error(self):
        d = LazyDictionary({'foo': lambda s: s['foo']})
        self.assertRaises(CircularReferenceError, d.__getitem__, 'foo')

    def test_constant_redefinition_error(self):
        d = LazyDictionary({
            'a': 1,
            'b': 2,
            'sum': lambda s: s['a'] + s['b'],
        })
        x = d['sum']
        self.assertRaises(ConstantRedefinitionError, d.__setitem__, 'a', 'foo')
        self.assertRaises(ConstantRedefinitionError, d.__delitem__, 'a')

    def test_lazy_evaluation(self):
        d = LazyDictionary({'sum': lambda s: s['a'] + s['b']})
        d['a'] = 1
        d['b'] = 2
        self.assertEqual(d['sum'], 3)

    def test_str(self):
        d =        LazyDictionary({'a': 1})
        self.assertEqual(str(d), "{'a': 1}")

    def test_repr(self):
        d =                        LazyDictionary({'a': 1})
        self.assertEqual(repr(d), "LazyDictionary({'a': 1})")

    def test_fibonacci(self):
        def fib_closure(d, i):
            return lambda d: d[str(i - 2)] + d[str(i - 1)]

        f = LazyDictionary({'0': 1, '1': 1})
        for i in range(2, 100):
            f[str(i)] = fib_closure(f, i)

        self.assertEqual(f['99'], 354224848179261915075)
