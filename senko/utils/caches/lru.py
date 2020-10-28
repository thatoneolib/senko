from .cache import Cache


class LRUCache(Cache):
    """
    A Least Recently Used (LRU) cache implementation.

    An item is considered used when it is acquired from the
    cache through :meth:`LRUCache.get`, ``cache[key]`` or
    when it is updated by :meth:`LRUCache.put`.

    When adding an item would exceed the cache's ``maxsize``,
    the least recently used item is evicted.

    Inherits from :class:`~.Cache`.
    
    Parameters
    ----------
    maxsize: int
        The maximum size of the cache.
    """

    def _evict(self):
        self._data.popitem(last=False)

    def get(self, key, fallback=None):
        try:
            self._data.move_to_end(key)
            return self._data[key]
        except KeyError:
            return fallback

    def put(self, key, value):
        if key not in self._data and len(self._data) + 1 > self._maxsize:
            self._evict()

        self._data[key] = value
        self._data.move_to_end(key)

    def __getitem__(self, key):
        self._data.move_to_end(key)
        return self._data[key]

