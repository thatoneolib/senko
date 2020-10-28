import collections


class Cache(object):
    """
    Base class for cache implementations.

    When adding an item would exceed the cache's ``maxsize``,
    the first item in the cache is evicted.

    Implements the following operations:

    .. container:: operations

        .. describe:: cache[x]

            Returns a value from the cache.

        .. describe:: cache[x] = y

            Adds a value to the cache.

        .. describe:: del cache[x]

            Remove a value from the cache.
        
        .. describe:: x in cache

            Checks whether a key is in the cache.
        
        .. describe:: len(cache)

            Returns the current size of the cache.

    Parameters
    ----------
    maxsize: int
        The maximum size of the cache.
    """

    def __init__(self, maxsize):
        self._data = collections.OrderedDict()
        self._maxsize = maxsize

    # Properties.

    @property
    def size(self):
        """
        int: The current size of the cache.
        """
        return len(self._data)

    @property
    def maxsize(self):
        """
        int: The maximum size of the cache.
        """
        return self._maxsize

    # Private methods.

    def _evict(self):
        """
        Evict an item from the cache. This method is called whenever
        a new item is about to be added to the cache, which would cause
        the cache to exceed its ``maxsize``.
        """
        self._data.popitem(last=False)

    # Public methods.

    def get(self, key, fallback=None):
        """
        Get an item from the cache.

        If ``key`` is not in the cache, return ``fallback`` instead.

        Parameters
        ----------
        key: Any
            The key to look up in the cache.
        fallback: Optional[Any]
            The fallback value to return when the requested
            item is not found. Defaults to ``None``.
        
        Returns
        -------
        Any
            The value of the requested item, or ``fallback`` when
            ``key`` is not found in the cache.
        """
        try:
            return self._data[key]
        except KeyError:
            return fallback

    def has(self, key):
        """
        Check whether the cache contains an item.

        Parameters
        ----------
        key: Any
            The key to check for.
        
        Returns
        -------
        bool
            ``True`` when the item is found, otherwise ``False``.
        """
        try:
            self._data[key]  # pylint: disable=pointless-statement
            return True
        except KeyError:
            return False

    def put(self, key, value):
        """
        Add an item to the cache.

        Parameters
        ----------
        key: Any
            The key to store the item under.
        value: Any
            The value of the tem.
        """
        if key not in self._data and len(self._data) + 1 > self._maxsize:
            self._evict()
        
        self._data[key] = value

    def clear(self):
        """
        Empties the cache.
        """
        self._data.clear()

    def pop(self, key):
        """
        Remove an item from the cache and return its value.

        Parameters
        ----------
        key: Any
            The key to pop from the cache.

        Raises
        ------
        KeyError
            When ``key`` is not in the cache.
        
        Returns
        -------
        Any
            The value of the removed item.
        """
        return self._data.pop(key)

    def remove(self, key, fallback=None):
        """
        Remove an item from the cache and return its value.

        Parameters
        ----------
        key: Any
            The key to remove from the cache.
        fallback: Optional[Any]
            The fallback value to return when the key is not in the cache.

        Returns
        -------
        Any
            The value of the removed item, or ``fallback`` if ``key``
            is not in the cache.
        """
        return self._data.pop(key, fallback)

    # Magic methods.

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        self.pop(key)

    def __contains__(self, key):
        return self.has(key)

    def __len__(self):
        return self.size

    def __repr__(self):
        name = self.__class__.__name__
        size = self.size
        maxsize = self.maxsize
        return f"<{name} size={size} maxsize={maxsize}>"
