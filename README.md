# memoization
 Memoization with unit tests in Python

A general introduction to memoization: https://en.wikipedia.org/wiki/Memoization

The memoization function allows to cache another function's results for later retrieval. 
Useful for expensive functions, where it is economical not to re-run the same function
and instead retreive the result, provided the input arguments are the same.

This memoization function has a timeout, which allows to clear cached results after
a certain number of milliseconds.

The memoization function is accompanied by a test_memoization.py file which contains a
number of tests to ensure this function works well.
