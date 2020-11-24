import datetime
import io
import traceback

import discord
import senko
from babel.dates import format_timedelta
from discord.ext import commands

from .helpers import count_calls, hint_for_command

__all__ = (
    "handle_command_not_found",
    "handle_command_on_cooldown",
    "handle_disabled_command",
)

# Invocation errors

async def handle_command_not_found(ctx, exc):
    """
    Exception handler for :exc:`~discord.ext.commands.CommandNotFound`.

    Quietly ignores the error.
    """
    return

@count_calls(10, commands.BucketType.member)
async def handle_command_on_cooldown(ctx, exc, calls=0):
    """
    Exception handler for :exc:`~discord.ext.commands.CommandOnCooldown`.

    Informs the user of the remaining cooldown.

    Has a cooldown of 10 seconds per member.
    """
    if calls > 0:
        return

    _ = ctx.locale

    # NOTE: Title of the error message displayed when a command is on cooldown.
    title = _("{e:error} Command on Cooldown")

    # NOTE: Text of the error message displayed when a command is on cooldown.
    # NOTE: "delay" is a localized period of time like "1 minute" or "5 seconds".
    text = _("**{user}**, `{command}` is on cooldown. Please try again in {delay}.")

    delta = datetime.timedelta(seconds=max(exc.retry_after, 1))
    delay = format_timedelta(delta, threshold=1.5, locale=_.language)

    title = ctx.bot.emotes.format(title)
    text = text.format(
        user=ctx.display_name,
        command=ctx.command.qualified_name,
        delay=delay
    )

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=10,
    )

@count_calls(30, commands.BucketType.channel)
async def handle_disabled_command(ctx, exc, calls=0):
    """
    Exception handler for :exc:`~discord.ext.commands.DisabledCommand`.

    Informs the user that the command is disabled.

    Has a cooldown of 30 seconds per channel.
    """
    if calls > 0:
        return

    _ = ctx.locale

    # NOTE: Title of the error message for disabled commands.
    title = _("{e:error} Command Disabled")

    # NOTE: Text of the error message for disabled commands.
    text = _("**{user}**, `{command}` is currently disabled.")

    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name, command=ctx.command.qualified_name)

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=10,
    )
