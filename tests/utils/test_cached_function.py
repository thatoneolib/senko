# pylint: disable=global-variable-undefined
import time
import asyncio
import pytest

from utils import caching

def setup_function(function):
    global _value
    _value = 1

def teardown_function(function):
    global _value 
    del _value

# helpers

def nullkey(*args, **kwargs):
    return None

# sync tests

def test_cached_function():
    global _value
    _value = 1

    @caching.cached_function(caching.Cache(128))
    def cached():
        return _value
    
    assert cached() == 1
    _value += 1
    assert cached() == 1

def test_cached_function_args():
    global _value
    _value = 1

    @caching.cached_function(caching.Cache(128))
    def cached(arg):
        return _value
    
    assert cached(1) == 1
    _value += 1
    assert cached(1) == 1
    assert cached(2) == 2

def test_cached_function_ignore_args():
    global _value
    _value = 1

    @caching.cached_function(caching.Cache(128), key=nullkey)
    def cached(arg):
        return _value

    assert cached(1) == 1
    assert cached(2) == 1
    _value += 1
    assert cached(1) == 1
    assert cached(2) == 1

# async tests

def test_async_cached_function(event_loop):
    global _value
    _value = 1

    @caching.cached_function(caching.Cache(128))
    async def cached():
        return _value
    
    assert asyncio.run(cached()) == 1
    _value += 1
    assert asyncio.run(cached()) == 1

def test_async_cached_function_args(event_loop):
    global _value
    _value = 1

    @caching.cached_function(caching.Cache(128))
    async def cached(arg):
        return _value
    
    assert asyncio.run(cached(1)) == 1
    _value += 1
    assert asyncio.run(cached(1)) == 1
    assert asyncio.run(cached(2)) == 2

def test_async_cached_function_ignore_args():
    global _value
    _value = 1

    @caching.cached_function(caching.Cache(128), key=nullkey)
    async def cached(arg):
        return _value

    assert asyncio.run(cached(1)) == 1
    assert asyncio.run(cached(2)) == 1
    _value += 1
    assert asyncio.run(cached(1)) == 1
    assert asyncio.run(cached(2)) == 1

