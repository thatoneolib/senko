from discord.ext import commands


class CogOverrides(commands.CogMeta):
    """
    Metaclass that inherits from :class:`discord.ext.commands.CogMeta`
    that adds support for the class parameters ``category`` and ``hidden``.
    """

    def __new__(cls, *args, **kwargs):
        cog_category = kwargs.pop("category", None)
        cog_hidden = kwargs.pop("hidden", False)
        new = super().__new__(cls, *args, **kwargs)

        # Get and set new attributes.
        new.__cog_category__ = cog_category
        new.__cog_hidden__ = cog_hidden

        for base in reversed(cls.__mro__):
            for attr, value in base.__dict__.items():
                if attr == "__cog_category__":
                    new.__cog_category__ = value
                elif attr == "__cog_hidden__":
                    new.__cog_hidden__ = value

        return new