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
        d = lazydict.LazyDictionary({'a': 1})
        self.assertEqual(str(d),   "{'a': 1}")

    def test_repr(self):
        d =               lazydict.LazyDictionary({'a': 1})
        self.assertEqual(repr(d), "LazyDictionary({'a': 1})")
