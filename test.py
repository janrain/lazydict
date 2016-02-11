from unittest import TestCase
import lazydict

class TestLazyDictionary(TestCase):

    def test_circular_reference_error(self):
        d = lazydict.LazyDictionary()
        d['foo'] = lambda s: s['foo']
        self.assertRaises(lazydict.CircularReferenceError, d.__getitem__, 'foo')

    def test_constant_redefinition_error(self):
        d = lazydict.LazyDictionary()
        d['a'] = 1
        d['b'] = 2
        d['sum'] = lambda s: s['a'] + s['b']
        x = d['sum']
        self.assertRaises(lazydict.ConstantRedefinitionError, d.__setitem__, 'a', 'hotdog')
        self.assertRaises(lazydict.ConstantRedefinitionError, d.__delitem__, 'a')

    def test_lazy_evaluation(self):
        d = lazydict.LazyDictionary()
        d['sum'] = lambda s: s['a'] + s['b']
        d['a'] = 1
        d['b'] = 2
        self.assertEqual(d['sum'], 3)

    def test_str(self):
        d = lazydict.LazyDictionary({'a': {'b': 1}})
        self.assertEqual(str(d),   "{'a': {'b': 1}}")

    def test_repr(self):
        d =               lazydict.LazyDictionary({'a': {'b': 1}})
        self.assertEqual(repr(d), "LazyDictionary({'a': {'b': 1}})")

    def test_atomic_evaluation(self):
        d = lazydict.LazyDictionary()
        d['division'] = lambda: 1/0
        self.assertEqual(d.states['division'], 'defined')
        self.assertRaises(ZeroDivisionError, d.__getitem__, 'division')
        # second call checks lazydict.CircularReferenceError is not raised.
        self.assertRaises(ZeroDivisionError, d.__getitem__, 'division')
        self.assertEqual(d.states['division'], 'error')
