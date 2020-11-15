import logging

import discord
from discord.ext import commands

from .overrides import CogOverrides


class Cog(commands.Cog, metaclass=CogOverrides):
    """
    A modified :class:`discord.ext.commands.Cog` implementation.

    Inherits from :class:`discord.ext.commands.Cog`.

    Parameters
    ----------
    bot: senko.Senko
        The bot instance.

    Attributes
    ----------
    bot: senko.Senko
        The bot instance.
    log: logging.Logger
        A logger instance for the cog.
    """

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.log = logging.getLogger(self.__module__)

    def __repr__(self):
        return f"<senko.cog name={self.qualified_name} hidden={self.hidden} category={self.category}>"

    @property
    def category(self):
        """
        Optional[Cog]: The cog under which the commands of this cog should be
        listed.

        This can be ``None`` when the cog does not have a category,
        or when the category cog is not found.

        Raises
        ------
        RuntimeError
            When a cyclic reference is found during category resolution.
        """
        # pylint: disable=no-member
        if self.__cog_category__ is None:
            return None

        cog = self.bot.get_cog(self.__cog_category__)
        if cog is None:
            return None

        traversed = set()
        while cog.category is not None:
            if cog in traversed:
                raise RuntimeError(f"Circular category reference for cog {self!r}: {cog!r}!")

            traversed.add(cog)
            cog = cog.category

        return cog

    @property
    def hidden(self):
        """
        bool: Whether this cog should be shown in the help command.
        """
        # pylint: disable=no-member
        return self.__cog_hidden__

    @discord.utils.cached_property
    def locale_id(self):
        """
        The base ID for translatable messages related to a cog.

        This ID, when combined with a valid suffix, can be used to
        look up translated attributes of a cog.

        Format: ``#cog_<lowercase_class_name>``.

        Examples
        --------

        ======================= ================================================
        Qualified Name          Locale ID
        ======================= ================================================
        ``Meta``                ``#cog_meta``
        ``Meta Commands``       ``#cog_meta_commands``
        ======================= ================================================

        For example, to look up the localized qualified name of
        a given cog, you would use ``#cog_<qualified_name>_name``.

        Returns
        -------
        str
            The message ID as described.
        """
        key = self.qualified_name.casefold().replace(" ", "_")
        return f"#cog_{key}"

    def get_qualified_name(self, locale=None):
        """
        Get the cog's specified name.

        Parameters
        ----------
        locale: Optional[senko.Locale]
            A locale to localize the name with.

        Returns
        -------
        str
            The qualified cog name.
        """
        if locale is None:
            return self.qualified_name
        else:
            return locale(f"{self.locale_id}_name")

    def get_description(self, locale=None):
        """
        Get the cog's description.

        Parameters
        ----------
        locale: Optional[senko.Locale]
            A locale to localize the description with.

        Returns
        -------
        Optional[str]
            The cog's description.
        """
        if locale is None:
            return self.description
        elif self.description:
            return locale(f"{self.locale_id}_description")
        else:
            return None
