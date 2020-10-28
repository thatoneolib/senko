# pylint: disable=global-variable-undefined
import time
import pytest

from senko.utils.caching import Cache, LRUCache, TTLCache

@pytest.mark.parametrize("cache", [Cache(1), LRUCache(1), TTLCache(1, ttl=60)])
def test_insert(cache):
    assert len(cache) == 0
    assert cache.size == 0
    assert cache.maxsize == 1

    cache.put(1, 1)
    assert len(cache) == 1
    assert cache.size == 1
    assert cache.get(1) == 1
    assert cache[1] == 1
    assert 1 in cache

    cache.put(2, 2)
    assert len(cache) == 1
    assert cache.size == 1
    assert cache.get(2) == 2
    assert cache[2] == 2
    assert 2 in cache
    assert 1 not in cache

@pytest.mark.parametrize("cache", [Cache(2), LRUCache(2), TTLCache(2, ttl=60)])
def test_evict(cache):
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)

    assert len(cache) == 2
    assert cache.size == 2
    assert 2 not in cache or 1 not in cache
    assert 3 in cache

@pytest.mark.parametrize("cache", [Cache(2), LRUCache(2), TTLCache(2, ttl=60)])
def test_clear(cache):
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)

    cache.clear()
    assert len(cache) == 0
    assert cache.size == 0


@pytest.mark.parametrize("cache", [Cache(2), LRUCache(2), TTLCache(2, ttl=60)])
def test_pop(cache):
    cache.put(1, 1)
    cache.put(2, 2)

    assert 1 == cache.pop(1)
    assert len(cache) == 1
    assert 2 == cache.pop(2)
    assert len(cache) == 0

    with pytest.raises(KeyError):
        cache.pop(0)
    with pytest.raises(KeyError):
        cache.pop(1)
    with pytest.raises(KeyError):
        cache.pop(2)

@pytest.mark.parametrize("cache", [Cache(2), LRUCache(2), TTLCache(2, ttl=60)])
def test_remove(cache):
    cache.put(1, 1)
    cache.put(2, 2)

    assert 1 == cache.remove(1)
    assert 2 == cache.remove(2)
    assert 0 == cache.remove(1, 0)

    assert cache.remove(1) is None

def test_lru_behavior():
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    lru.get(1)

    lru.put(3, 3)
    assert 1 in lru
    assert 2 not in lru
    assert 3 in lru

def test_ttl_behavior():
    ttl = TTLCache(2, ttl=0.05)
    ttl.put(1, 1)
    ttl.put(2, 2)
    time.sleep(0.05)
    assert ttl.get(1) is None
    assert ttl.get(2) is None
    assert ttl.size == 0