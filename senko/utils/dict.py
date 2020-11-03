
class CaseInsensitiveDict(dict):
    """
    A case insensitive :class:`dict` implementation.

    Key assignments and lookups are made case-insensitive,
    using the :meth:`str.casefold` method to normalize the
    keys.

    The key behavior aside, functions mostly like a regular
    :class:`dict`.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k in list(self.keys()):
            self[k] = super(CaseInsensitiveDict, self).pop(k)

    def __contains__(self, key):
        return super().__contains__(key.casefold())

    def __delitem__(self, key):
        return super().__delitem__(key.casefold())

    def __getitem__(self, key):
        return super().__getitem__(key.casefold())

    def __setitem__(self, key, value):
        super().__setitem__(key.casefold(), value)

    def get(self, key, default=None):
        """
        Get a value from the dictionary.

        Parameters
        ----------
        key: Any
            The key to look up.
        default: Optional[Any]
            An optional default value to return if ``key`` is not
            in the dictionary.

        Returns
        -------
        Any
            The value for ``key``, if ``key`` is in the dictionary,
            otherwise ``default``.
        """
        return super().get(key.casefold(), default)

    def pop(self, key, default=None):
        """
        Remove a key from the dictionary and return its value.

        Parameters
        ----------
        key: Any
            The key to remove.
        default: Optional[Any]
            An optional default value to return when ``key`` is not
            in the dictionary.

        Returns
        -------
        Any
            The value for ``key``, if ``key`` is in the dictionary,
            otherwise ``default``.
        """
        return super().pop(key.casefold(), default)

    def setdefault(self, key, default=None):
        """
        Insert ``key`` with a value of ``default`` if ``key`` is
        not in the dictionary.

        Parameters
        ----------
        key: Any
            The key to look up and return the value for.
        default: Optional[Any]
            The value to set for ``key`` if ``key`` is not in the
            dictionary.

        Returns
        -------
        Any
            The value for ``key`` or ``default`` if ``key`` was
            not in the dictionary.
        """
        return super().setdefault(key.casefold(), default)

    def update(self, *args, **kwargs):
        """
        Update the dictionary with another dictionary's contents or keywords.

        Parameters
        ----------
        other: Optional[Union[Dict[Any, Any], Iterable[Tuple[Any, Any]]
            An optional dictioary or iterable of key-value pairs to update
            this dictionary from.
        \*\*kwargs
            Optional key-value arguments to update this dictionary with.
        """
        # Handle arguments
        if len(args) > 1:
            raise TypeError(f"update expected at most 1 argument, got {len(args)}")
        elif len(args) == 1:
            other = args[0]

            if isinstance(other, dict):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value
        
        # Handle keyword arguments
        for key, value in kwargs.items():
            self[key] = value

