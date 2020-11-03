from discord.ext import commands

from .overrides import CommandOverrides


class Command(CommandOverrides, commands.Command):
    """
    A :class:`discord.ext.commands.Command` modified with
    :class:`senko.CommandOverrides`.
    """
    def __repr__(self):
        return f"<senko.Command qualified_name={self.qualified_name!r}>"
