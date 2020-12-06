from time import time
import uuid

# Creates a function that can memoize a result of a function
# Memoized (cached) results will be deleted if they exceed their timeout (millisec)
# If resolver is set to True, the memoize function will:
#  - clear any cached results that have timed out
#  - generate a uuid based on all arguments given to the original function
#  - check if this result is already cached and if so, return the cached result
#  - if result is not cached, cache it with uuid as the key
#  - return the result

# Create cache for storing memoized results
cache = {}


def memoize(func, resolver=False, timeout=-1):
    """

    :param func: function the results of which should be memoized
    :param resolver: set to True to memoize results. Set to False to disable memoization
    :param timeout: milliseconds after which memoized results should time out and be deleted from cache
    :return: result of func
    """
    if resolver is True:
        def resolver(*args):
            # Delete all timed-out values
            clean_cache(cache, timeout)

            # Generate uuid for key
            uuid = str(generate_uuid(*args))

            # If new result, update cache and return result
            if uuid not in cache.keys():
                new_result = func(*args)
                cache[uuid] = [new_result, millisec_timestamp_now()]
            return cache[uuid]
        return resolver
    # If no resolver provided, return original function
    else:
        return func


# Generate a uuid based on all function arguments
# Generates the same uuid for the same input
def generate_uuid(*args):
    key = ""
    for arg in args:
        key += repr(arg)
    return uuid.uuid3(uuid.NAMESPACE_DNS, key)


def millisec_timestamp_now():
    return int(round(time() * 1000))


# Deletes all cache values which have timed out
# Timeout in milliseconds
def clean_cache(cache, timeout):
    for key, value in list(cache.items()):
        if millisec_timestamp_now() - value[1] > timeout:
            cache.pop(key)
