import unittest
memoization = __import__("memoization")
cache = memoization.cache


# Helper test function
def test_func(*args):
    return 1


# Test memoization function
class TestMemoization(unittest.TestCase):
    # Output value of a function should be memoized
    def test_output_is_memoized(self):
        memoized = memoization.memoize(test_func, resolver=True, timeout=5000)
        result = memoized()
        self.assertEqual(result[0], cache['c87ee674-4ddc-3efe-a74e-dfe25da5d7b3'][0])

    # Cached results should be deleted after timeout
    def test_cache_results_cleared_after_timeout(self):
        # Set timeout to -1 to ensure values time out immediately after creation
        memoized = memoization.memoize(test_func, resolver=True, timeout=-1)
        memoized(1)

        # Known key for the above memoized cache entry
        key = 'afd0b036-625a-3aa8-b639-9dc8c8fff0ff'

        # Run memoize with resolver=True again with a different function input
        # This will clear cache of any timed-out values and insert new value
        memoized(2)
        self.assertNotIn(key, cache.keys())

    # Memoization function should work when resolver=False and no timeout specified
    # it should simply run the function with no memoization
    def test_memoize_func_if_resolver_is_not_provided(self):
        memoized = memoization.memoize(test_func)
        result = memoized(1)
        self.assertEqual(result, 1)

    # Test memoization key is different for different inputs
    def test_memoization_keys_are_different_for_different_inputs(self):
        memoized = memoization.memoize(test_func, resolver=True, timeout=5000)
        memoized(1)
        memoized(2)

        keys = []
        for key in cache.keys():
            keys.append(key)
        self.assertNotEqual(keys[0], keys[1])

    # Test function to be memoized can accept multiple args
    def test_func_with_multiple_args(self):
        memoized = memoization.memoize(test_func, resolver=True, timeout=5000)
        memoized(1)
        memoized(1, 2, 3)

    # Test function to be memoized can accept different types of args
    # Function should accept any Python object
    def test_func_with_different_arg_types(self):
        memoized = memoization.memoize(test_func, resolver=True, timeout=5000)
        arg_types = {'str': "a",
                     'int': 1,
                     'float': 1.1,
                     'list': [1, 1],
                     'tuple': (1, 1),
                     'dict': {"1": 1},
                     'set': {"1", "2"},
                     'bytes': b'1',
                     'bool': True,
                     'NoneType': None,
                     'function': test_func
                     }

        for arg in arg_types.values():
            memoized(arg)


if __name__ == '__main__':
    unittest.main()
