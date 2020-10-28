import time
from .lru import LRUCache


class TTLCache(LRUCache):
    """
    A LRU Cache with a time-to-live for added items.

    Each item added to this cache is assigned a time-to-live.
    Once an items time-to-live has expired, they are no longer
    accessible and will be evicted from the cache.

    When adding a key would exceed the ``maxsize`` of the
    cache, and no expired items can be evicted, the least recently
    used item is removed instead.

    Inherits from :class:`~.Cache`.

    Parameters
    ----------
    maxsize: int
        The maximum size of the cache.
    ttl: float
        The time-to-live of cache items.
    """

    def __init__(self, maxsize, ttl):
        super().__init__(maxsize)
        self._ttl = ttl

    @property
    def size(self):
        self._expire()
        return super().size

    def _expire(self, now=None):
        """
        Remove expired items from the cache.
        """
        if now is None:
            now = time.time()

        items = list(self._data.items())
        expired = [k for k, v in items if now - v[1] > self._ttl]
        for k in expired:
            self._data.pop(k, None)

    def get(self, key, fallback=None):
        self._expire()
        value, _ = super().get(key, fallback=(fallback, 0))
        return value

    def put(self, key, value):
        now = time.time()
        self._expire(now)

        if key not in self._data and len(self._data) + 1 > self._maxsize:
            self._evict()

        self._data[key] = (value, now)
        self._data.move_to_end(key)
    
    def pop(self, key):
        value, _ = super().pop(key)
        return value

    def remove(self, key, fallback=None):
        value, _ = super().remove(key, fallback=(fallback, 0))
        return value

    def __getitem__(self, key):
        self._expire()
        self._data.move_to_end(key)
        return self._data[key][0]
