.. _utils_caches:

Caches
######

Senko comes with a set of simple cache implementations. These are generally
thread-safe, as their internal implementation does not make use of anything
that would not be thread-safe.

Cache
*****

The basic cache class from which all other cache implementations inherit.

.. autoclass:: senko.utils.Cache
    :members:

LRUCache
********

.. autoclass:: senko.utils.LRUCache

TTLCache
********

.. autoclass:: senko.utils.TTLCache
