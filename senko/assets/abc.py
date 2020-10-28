import abc
import logging
import os


class AssetLibrary(abc.ABC):
    """
    Base class for asset libraries.

    .. container:: operations

        .. describe:: len(x)

            Returns the amount of loaded assets.

        .. describe:: x[key]

            Returns the ``key`` asset.

    Parameters
    ----------
    sentinel: Optional[Any]
        The default value to return for missing assets.
        Defaults to ``None``.
    """

    def __init__(self, sentinel=None):
        self.logger = logging.getLogger("senko.assets")
        self.sentinel = sentinel
        self.objects = dict()
        self.missing = set()

    def load_file(self, file):
        """
        Load assets from a file.

        Must be implemented by subclasses.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file to load assets from.
        """
        raise NotImplementedError

    def load_dir(self, path, extensions, walk=True, ignore_errors=False):
        """
        Load all matching files found in the given directory.

        This method iterates over all the files found in the given
        path and calls :meth:`~senko.AssetLibrary.load_file` on them.

        Parameters
        ----------
        path: Union[str, os.PathLike]
            The path to the directory to load files from.
        extensions: Optional[List[str]]
            A list of file extensions to filter by. Only files whose extension
            is included in the list are attempted to be loaded.
        walk: Optional[bool]
            When set to ``True``, also scans any subdirectories of ``path`` for
            files. Defaults to ``True``.
        ignore_errors: Optional[bool]
            When set to ``True``, caught exceptions do not stop the loading
            process. Defaults to ``False``.
        """
        if walk:
            def generator(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        yield os.path.join(root, file)

        else:
            def generator(path):
                for file in os.listdir(path):
                    yield os.path.join(path, file)

        for file in generator(path):
            extension = os.path.splitext(file)[1][1:]
            if not extension in extensions:
                continue

            try:
                self.load_file(file)
            except Exception as exc:
                self.logger.exception(f"An error occured while loading {file!r}!", exc_info=exc)

                if not ignore_errors:
                    raise

    def get(self, key, fallback=None):
        """
        Get an asset by its key.

        If asset is not found, the fallback value, if specified,
        is returned instead. If not set, then the sentinel value
        is returned.

        In either case, a warning is logged.

        Parameters
        ----------
        key: str
            The asset key.
        fallback: Optional[Any]
            The fallback value to return if the key is not found.
        """
        try:
            return self.objects[key]
        except KeyError:
            self.logger.debug(f"The {key!r} key is missing!")
            self.add_missing(key)
            return fallback or self.sentinel

    def has(self, key):
        """
        Check whether the library has a key.

        Parameters
        ----------
        key: str
            The asset key.
        
        Returns
        -------
        bool
            ``True`` when found, otherwise ``False``.
        """
        return key in self.objects

    def keys(self):
        """
        List[str]: Returns a list of all asset keys.
        """
        return self.objects.keys()

    def values(self):
        """
        List[Any]: Returns a list of all loaded assets.
        """
        return self.objects.values()

    def items(self):
        """
        List[Tuple[str, Any]]: Returns a list over all key-asset pairs.
        """
        return self.objects.items()

    def length(self):
        """
        int: Returns the amount of loaded assets.
        """
        return len(self.objects)

    def clear(self):
        """
        Unloads all assets.
        """
        self.objects = dict()
        self.clear_missing()

    def add_missing(self, key):
        """
        Mark an asset as missing.

        Parameters
        ----------
        key: str
            The asset key.
        """
        self.missing.add(key)

    def get_missing(self):
        """
        Get the keys of all missing assets.

        Returns
        -------
        List[str]
            A list of asset keys.
        """
        return sorted(list(self.missing))

    def clear_missing(self):
        """
        Clear the missing key list.
        """
        self.missing = set()


    def __len__(self):
        return len(self.objects)

    def __getitem__(self, key):
        try:
            return self.objects[key]
        except KeyError:
            self.logger.debug(f"The {key!r} key is missing!")
            self.add_missing(key)
            raise
