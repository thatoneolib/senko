from discord.ext import commands

from .command import Command
from .group import Group


def command(*args, **kwargs):
    """
    A decorator that transforms a function into a :class:`senko.Command`.

    Internally propagates the call to :func:`discord.ext.commands.command`.
    """
    kwargs["cls"] = kwargs.get("cls", Command)
    return commands.command(*args, **kwargs)


def group(*args, **kwargs):
    """
    A decorator that transforms a function into a :class:`senko.Group`.

    Internally propagates the call to :func:`discord.ext.commands.command`.
    """
    kwargs["cls"] = kwargs.get("cls", Group)
    return commands.command(*args, **kwargs)
