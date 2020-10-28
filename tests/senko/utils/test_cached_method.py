import time
import asyncio
import pytest

from senko.utils import caching

# helpers

def nullkey(*args, **kwargs):
    return None

# sync tests

def test_cached_method():

    class Object:
        def __init__(self, value):
            self.value = value
            self.cache = caching.Cache(128)
        
        @caching.cached_method(lambda self: self.cache)
        def get(self):
            return self.value
    
    o1 = Object(1)
    assert o1.get() == 1
    o1.value = 2
    assert o1.get() == 1

    o2 = Object(2)
    assert o2.get() == 2
    o2.value = 3
    assert o2.get() == 2
    
def test_cached_method_args():

    class Object:
        def __init__(self, value):
            self.value = value
            self.cache = caching.Cache(128)
        
        @caching.cached_method(lambda self: self.cache)
        def get(self, arg):
            return self.value
    
    o1 = Object(1)
    assert o1.get(1) == 1
    o1.value = 2
    assert o1.get(1) == 1
    assert o1.get(2) == 2

    o2 = Object(2)
    assert o2.get(1) == 2
    o2.value = 3
    assert o2.get(1) == 2
    assert o2.get(2) == 3

def test_cached_method_ignore_args():

    class Object:
        def __init__(self, value):
            self.value = value
            self.cache = caching.Cache(128)
        
        @caching.cached_method(lambda self: self.cache, key=nullkey)
        def get(self, arg):
            return self.value

    o1 = Object(1)
    assert o1.get(1) == 1
    assert o1.get(2) == 1
    o1.value = 2
    assert o1.get(1) == 1
    assert o1.get(2) == 1

    o2 = Object(1)
    assert o2.get(1) == 1
    assert o2.get(2) == 1
    o2.value = 2
    assert o2.get(1) == 1
    assert o2.get(2) == 1
    
# async tests

def test_async_cached_method(event_loop):

    class Object:
        def __init__(self, value):
            self.value = value
            self.cache = caching.Cache(128)
        
        @caching.cached_method(lambda self: self.cache)
        async def get(self):
            return self.value
    
    o1 = Object(1)
    assert asyncio.run(o1.get()) == 1
    o1.value = 2
    assert asyncio.run(o1.get()) == 1

    o2 = Object(2)
    assert asyncio.run(o2.get()) == 2
    o2.value = 3
    assert asyncio.run(o2.get()) == 2
    
def test_async_cached_method_args(event_loop):

    class Object:
        def __init__(self, value):
            self.value = value
            self.cache = caching.Cache(128)
        
        @caching.cached_method(lambda self: self.cache)
        async def get(self, arg):
            return self.value
    
    o1 = Object(1)
    assert asyncio.run(o1.get(1)) == 1
    o1.value = 2
    assert asyncio.run(o1.get(1)) == 1
    assert asyncio.run(o1.get(2)) == 2

    o2 = Object(2)
    assert asyncio.run(o2.get(1)) == 2
    o2.value = 3
    assert asyncio.run(o2.get(1)) == 2
    assert asyncio.run(o2.get(2)) == 3

def test_async_cached_method_ignore_args(event_loop):

    class Object:
        def __init__(self, value):
            self.value = value
            self.cache = caching.Cache(128)
        
        @caching.cached_method(lambda self: self.cache, key=nullkey)
        async def get(self, arg):
            return self.value

    o1 = Object(1)
    assert asyncio.run(o1.get(1)) == 1
    assert asyncio.run(o1.get(2)) == 1
    o1.value = 2
    assert asyncio.run(o1.get(1)) == 1
    assert asyncio.run(o1.get(2)) == 1

    o2 = Object(1)
    assert asyncio.run(o2.get(1)) == 1
    assert asyncio.run(o2.get(2)) == 1
    o2.value = 2
    assert asyncio.run(o2.get(1)) == 1
    assert asyncio.run(o2.get(2)) == 1
    