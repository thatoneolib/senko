import json
import logging

from .abc import AssetLibrary


class Images(AssetLibrary):
    """
    :class:`AssetLibrary` for strings containing image URLs.

    Parameters
    ----------
    sentinel: Optional[str]
        The fallback value that is returned when a requested image is not found.
        Should be the URL of an image.

        Defaults to ``None``.
    """

    def __init__(self, sentinel=None):
        super().__init__(sentinel=sentinel)
        self.log = logging.getLogger("senko.assets.images")

    def load_file(self, file):
        """
        Load images from a file.
        
        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file to load.
        """
        with open(file, "r", encoding="utf-8") as fileobj:
            data = json.load(fileobj)

        index = dict()
        for key, value in data.items():
            if not isinstance(key, str):
                t = type(key).__name__
                raise TypeError(f"Bad type {t!r} for image key (must be str)!")

            if not isinstance(value, str):
                t = type(key).__name__
                raise TypeError(f"Bad type {t!r} for url of image {key!r} (must be str)!")

            index[key] = value

        self.objects.update(index)

    def load_dir(self, path, walk=True, ignore_errors=False):
        """
        Walk through a directory and attempt to load all JSON-files in it.

        Parameters
        ----------
        path: Union[str, os.PathLike]
            The directory path.
        walk: Optional[bool]
            Whether to walk the directory tree. Defaults to ``True``.
        ignore_errors: Optional[bool]
            Whether to not stop upon encountering errors.
        """
        before = len(self.objects)
        super().load_dir(path, ["json"], walk=walk, ignore_errors=ignore_errors)
        after = len(self.objects)

        if after > before:
            diff = after - before
            self.log.info(f"Loaded {diff} image(s).")
