import json
import logging
import re
import string

import discord

from .abc import AssetLibrary

__all__ = ("EmojiFormatter", "Emojis")

# The default fallback value that is returned when requesting
# a missing emoji. In Discord on desktop, this is the red question mark.
SENTINEL = "\N{BLACK QUESTION MARK ORNAMENT}"


class EmojiFormatter(string.Formatter):
    """
    A custom :class:`string.Formatter` that replaces ``{e:key}`` template
    strings with an emoji retrieved through :meth:`EmojiLibrary.get`.

    Positional and keyword parameters passed into :meth:`EmojiFormatter.format`
    are formatted as usual, and are expected to resolve any other template
    strings found within the provided format string.

    .. _formatter: https://docs.python.org/3/library/string.html#string.Formatter

    .. note::

        See `string.Formatter <formatter>`_ for information on string formatters.

    Parameters
    ----------
    emoji_library: EmojiLibrary
        The emoji library to draw emojis from.
    """

    def __init__(self, emoji_library):
        self.emojis = emoji_library

    def format(self, format_string, *args, **kwargs):
        formatted = self.vformat(format_string, args, kwargs)
        formatted = formatted.format(*args, **kwargs)
        return formatted

    def get_value(self, key, args, kwargs):
        return key

    def convert_field(self, value, conversion):
        if conversion is None:
            return value
        else:
            return f"{value}!{conversion}"

    def format_field(self, value, format_spec):
        if value == "e":
            if format_spec != "":
                return str(self.emojis.get(format_spec))
            else:
                return f"{{{value}}}"
        elif format_spec != "":
            return f"{{{value}:{format_spec}}}"
        else:
            return f"{{{value}}}"

    def get_field(self, field_name, args, kwargs):
        return field_name, None


class Emojis(AssetLibrary):
    """
    :class:`AssetLibrary` for :class:`discord.PartialEmoji` objects.

    Creates :class:`discord.PartialEmoji` objects from JSON-files.
    
    Parameters
    ----------
    sentinel: Optional[Union[str, discord.PartialEmoji, discord.Emoji]]
        The fallback value that is returned when a requested emoji is not
        found. Should be either a string of a unicode emoji, or any of the
        emoji types found in ``discord.py``.

        Defaults to \N{BLACK QUESTION MARK ORNAMENT}.
    """

    def __init__(self, sentinel=None):
        super().__init__(sentinel=sentinel or SENTINEL)
        self.logger = logging.getLogger("senko.emojis")
        self.formatter = EmojiFormatter(self)

    def load_file(self, file):
        """
        Load emojis from a file.

        Expects the file to be in JSON format, containing a single map that
        maps strings to strings, which can either be unicode or discord emojis.   

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file to load.
        """
        with open(file, "r", encoding="utf-8") as fileobj:
            data = json.load(fileobj)

        index = dict()
        pattern = re.compile(r"<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$")

        for key, value in data.items():
            if not isinstance(key, str):
                t = type(key).__name__
                raise TypeError(f"Bad type {t!r} for emoji key (must be str)!")
            
            if not isinstance(value, str):
                t = type(key).__name__
                raise TypeError(f"Bad type {t!r} for value of emoji {key!r} (must be str)!")

            match = pattern.match(value)

            if match:
                anim = bool(match.group(1))
                name = match.group(2)
                id = int(match.group(3))
                partial = discord.PartialEmoji(animated=anim, name=name, id=id)
            else:
                partial = discord.PartialEmoji(animated=False, name=value, id=None)

            index[key] = partial

        self.objects.update(index)

    def load_dir(self, path, walk=True, ignore_errors=False):
        """
        Walk through a directory and attempt to load all json files in it.

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
            self.logger.info(f"Loaded {diff} emoji(s).")

    def format(self, string, *args, **kwargs):
        """
        Format a string with emojis and the provided parameters.

        Replaces template substrings like ``{e:key}`` with the corresponding
        emoji. Missing emojis are logged and are replaced with the sentinel
        value instead.

        Example
        -------
        .. code-block:: python3

            string = "{e:senko} Senko likes {e:aburaage} Tofu."
            string = bot.emojis.format(string)

        Parameters
        ----------
        string: str
            The string to format.
        
        Returns
        -------
        str
            The formatted string.
        """
        return self.formatter.format(string, *args, **kwargs)
