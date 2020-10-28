import time
import inspect
import functools

__all__ = ("hash_key", "cached_function", "cached_method", "cached_property")

# pylint: disable=function-redefined

_marker = (object(),)


def hash_key(*args, **kwargs):
    r"""
    Get a unique key for a combination of positional and
    keyword arguments.

    Parameters
    ----------
    \*args
        Positional arguments.
    \*\*kwargs
        Keyword arguments.
    
    Returns
    -------
    int
        A unique hash value generated for the provided
        positional and keyword arguments.
    """
    key = args
    if kwargs:
        key += _marker + tuple(kwargs.items())

    return hash(key)


def cached_function(cache, key=hash_key, lock=None):
    """
    Decorator that adds caching to a decorated function.

    Examples
    --------

    .. code-block:: python3

        from senko.utils import caching

        @caching.cached_function(caching.TTLCache(64, 60))
        def get_cool_person(name):
            print("Determining a really cool person...")
            return f"You're cool, {name}!"

        cool = get_cool_person("Maxee")
        print(cool)
        cool = get_cool_person("Maxee")
        print(cool)

        # Prints:
        # Determining a really cool person...
        # You're cool, Maxee!
        # You're cool, Maxee!

    Parameters
    ----------
    cache: ~senko.utils.caching.Cache
        A cache to use to store function values in.
    key: Optional[Callable[[Any, ...], Any]
        A callable that takes any set of positional and
        keyword arguments and returns a unique key. Defaults
        to :func:`~senko.utils.caching.hash_key`.
    lock: Optional[Union[asyncio.Lock, threading.Lock]]
        An optional lock to use when interacting with the cache.
        Must be a lock corresponding to the type of the decorated
        function. Defaults to ``None``, disabling the lock.
    """

    def decorator(func):

        # Asynchronous wrapper with lock
        if inspect.iscoroutinefunction(func) and lock is not None:
            async def wrapper(*args, **kwargs):
                k = key(*args, **kwargs)
                try:
                    async with lock:
                        return cache[k]
                except KeyError:
                    async with lock:
                        cache[k] = v = await func(*args, **kwargs)
                    return v

        # Asynchronous wrapper without lock:
        if inspect.iscoroutinefunction(func):
            async def wrapper(*args, **kwargs):
                k = key(*args, **kwargs)
                try:
                    return cache[k]
                except KeyError:
                    cache[k] = v = await func(*args, **kwargs)
                    return v

        # Synchronous wrapper with lock
        elif lock is not None:
            def wrapper(*args, **kwargs):
                k = key(*args, **kwargs)
                try:
                    with lock:
                        return cache[k]
                except:
                    with lock:
                        cache[k] = v = func(*args, **kwargs)
                    return v

        # Synchronous wrapper without lock
        else:
            def wrapper(*args, **kwargs):
                k = key(*args, **kwargs)
                try:
                    return cache[k]
                except:
                    cache[k] = v = func(*args, **kwargs)
                    return v

        return functools.update_wrapper(wrapper, func)

    return decorator


def cached_method(cache, key=hash_key, lock=None, slot=None):
    """
    Decorator that adds caching to a decorated method.

    Example
    -------

    .. code-block:: python3

        from senko.utils import caching

        class Example:
            def __init__(self):
                self._cache = caching.LRUCache(128)
            
            @caching.cached_method(lambda self: self._cache)
            def greeting(self, name):
                print("Generating highly personalized greeting.")
                return f"Hello {name}!"
        
        example = Example()
        print(example.greeting("Maxee"))
        print(example.greeting("Maxee"))

        # Prints:
        # Generating highly personalized greeting.
        # Hello Maxee!
        # Hello Maxee!

    Parameters
    ----------
    cache: Callable[[Any], ~senko.utils.caching.Cache]
        A callable that takes an instance of the method's class
        as its sole parameter and returns a cache instance.
    key: Optional[Callable[[Any, ...], Any]
        A callable that takes any set of positional and
        keyword arguments and returns a unique key. Defaults
        to :func:`~senko.utils.caching.hash_key`.
    lock: Optional[Union[asyncio.Lock, threading.Lock]]
        An optional lock to use when interacting with the cache.
        Must be a lock corresponding to the type of the decorated
        method. Defaults to ``None``, disabling the lock.
    """

    def decorator(func):

        # Asynchronous wrapper with lock
        if inspect.iscoroutinefunction(func) and lock is not None:
            async def wrapper(self, *args, **kwargs):
                c = cache(self)
                k = key(self, *args, **kwargs)
                try:
                    async with lock:
                        return c[k]
                except KeyError:
                    async with lock:
                        c[k] = v = await func(self, *args, **kwargs)
                    return v

        # Asynchronous wrapper without lock:
        if inspect.iscoroutinefunction(func):
            async def wrapper(self, *args, **kwargs):
                c = cache(self)
                k = key(*args, **kwargs)
                try:
                    return c[k]
                except KeyError:
                    c[k] = v = await func(self, *args, **kwargs)
                    return v

        # Synchronous wrapper with lock
        elif lock is not None:
            def wrapper(self, *args, **kwargs):
                c = cache(self)
                k = key(*args, **kwargs)
                try:
                    with lock:
                        return c[k]
                except:
                    with lock:
                        c[k] = v = func(self, *args, **kwargs)
                    return v

        # Synchronous wrapper without lock
        else:
            def wrapper(self, *args, **kwargs): 
                c = cache(self)
                k = key(*args, **kwargs)
                try:
                    return c[k]
                except:
                    c[k] = v = func(self, *args, **kwargs)
                    return v

        return functools.update_wrapper(wrapper, func)

    return decorator


class cached_property(object):
    """
    A decorator class that turns a function into a cached property.

    Examples
    --------

    .. code-block:: python3

        class Addition:
            \"\"\"
            Add two numbers.

            Parameters
            ----------
            a: int
                The first number.
            b: int
                The second number.
            \"\"\"
            def __init__(self, a, b):
                self.a = a
                self.b = b

            @cached_property()
            def result(self):
                \"\"\"
                int: The result of the addition.
                \"\"\"
                # This function is ran exactly once when accessed.
                return a + b
    
    Parameters
    ----------
    slot: Optional[str] 
        Optional name of an attribute slot to use to store the cached
        property value in. Defaults to ``__<function name>_cache__``.
    ttl: Optional[float]
        An optional delay in seconds after which the next call to the
        property will call the decorated function again to determine
        the return value. Defaults to ``None``, disabling the timeout.
    """

    def __init__(self, slot=None, ttl=None):
        self._attr = slot
        self._func = None
        self._ttl = ttl

    def __get__(self, instance, owner):
        now = time.time()
        value, last = getattr(instance, self._attr, (None, 0))

        # Handle no timeout.
        if self._ttl is None and last == 0:
            value = self._func(instance)
            setattr(instance, self._attr, (value, now))

        elif self._ttl is None:
            value = getattr(instance, self._attr)[0]

        # Handle timeout.
        elif now - last > self._ttl:
            value = self._func(instance)
            setattr(instance, self._attr, (value, now))

        else:
            value = getattr(instance, self._attr)[0]

        return value

    def __call__(self, func):
        self._func = func
        self._attr = self._attr or f"__{func.__name__}_cache__"
        self.__doc__ = getattr(func, "__doc__")
        return self
