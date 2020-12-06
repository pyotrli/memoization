from time import time
import uuid


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


# Create cache for storing memoized results
cache = {}


def memoize(func, resolver=False, timeout=-1):
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
