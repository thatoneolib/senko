.. _utils_caching:

Caching
#######

Senko comes with a set of simple cache implementations and caching utilities.
These are generally thread-safe, unless explicitly stated otherwise, as their
internal implementation does not make use of anything that would not be
thread-safe.

Caching Decorators
******************

Senko provides a set of decorators that wrap functions with memoizing wrappers
functions. Function- and method-specific decorators allow you to specify a cache
to use for the values returned by the function. These decorators support both
normal and coroutine functions.

.. note::

    These decorators are greatly inspired by :py:func:`functools.lru_cache` and
    `cachetools <https://github.com/tkem/cachetools>`_, an excellent library for
    performant caching utilities.

.. autofunction:: utils.caching.hash_key
.. autofunction:: utils.caching.cached_function
.. autofunction:: utils.caching.cached_method
.. autofunction:: utils.caching.cached_property

Cache Implementations
*********************

For general use, Senko provides a set of simple cache implementations.

Cache
=====

The basic cache class from which all other cache implementations inherit.

.. autoclass:: utils.caching.Cache
    :members:

LRUCache
========

.. autoclass:: utils.caching.LRUCache

TTLCache
========

.. autoclass:: utils.caching.TTLCache
