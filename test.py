from unittest import TestCase
import lazydict

class TestLazyDictionary(TestCase):

    def test_circular_reference_error(self):
        d = lazydict.LazyDictionary()
        d['foo'] = lambda s: s['foo']
        with self.assertRaises(lazydict.CircularReferenceError):
            x = d['foo']

    def test_constant_redefinition_error(self):
        d = lazydict.LazyDictionary()
        d['a'] = 1
        d['b'] = 2
        d['sum'] = lambda s: s['a'] + s['b']
        x = d['sum']
        with self.assertRaises(lazydict.ConstantRedefinitionError):
            d['a'] = "hotdog"

        with self.assertRaises(lazydict.ConstantRedefinitionError):
            del d['a']

    def test_lazy_evaluation(self):
        d = lazydict.LazyDictionary()
        d['sum'] = lambda s: s['a'] + s['b']
        d['a'] = 1
        d['b'] = 2
        self.assertEqual(d['sum'], 3)
