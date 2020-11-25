import datetime
import io
import traceback

import discord
import senko
from babel.dates import format_timedelta
from discord.ext import commands

from .helpers import count_calls, hint_for_command

__all__ = (
    # Invocation errors
    "handle_command_not_found",
    "handle_command_on_cooldown",
    "handle_disabled_command",

    # Parameter and parsing errors
    "handle_bad_argument",
    "handle_missing_required_argument",
    "handle_too_many_arguments",

    # Quotation errors
    "handle_unexpected_quote_error",
    "handle_invalid_end_of_quoted_string_error",
    "handle_expected_closing_quote_error",
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

# Parameter and parsing errors

async def handle_bad_argument(ctx, exc):
    """
    Exception handler for :exc:`~discord.ext.commands.BadArgument`.

    Informs the user of the missing argument if the exception has a
    ``param`` attribute. Displays the command usage and help command
    invocation for the command.
    """
    _ = ctx.locale

    # NOTE: Title of the error message for bad or invalid parameters.
    title = _("{e:error} Invalid Parameter")

    if hasattr(exc, "param") and exc.param is not None:
        # NOTE: Text of the error message for bad or invalid parameters, when the
        # NOTE: faulty parameter is known. Error is replaced by the concrete
        # NOTE: error message given by the converter that failed.
        text = _(
            "**{user}**, you have entered an invalid value for the `{parameter}` "
            "parameter. {error}"
        )
    else:
        # NOTE: Text of the error message for bad or invalid parameters, when the
        # NOTE: faulty parameter is not known. Error is replaced by the concrete
        # NOTE: error message given by the converter that failed.
        text = _(
            "**{user}**, you have entered an invalid value for one of "
            "the parameters. {error}"
        )

    # Get variables
    prefix = ctx.default_prefix
    command_key = ctx.command.locale_id

    if hasattr(exc, "param") and exc.param is not None:
        param_key = f"{command_key}_parameter_{exc.param.name}"
        param_name = _(param_key)
    else:
        param_name = None

    # Format strings
    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name, parameter=param_name, error=exc)
    hint_field = hint_for_command(prefix, ctx.command, _)

    await ctx.embed(
        title=title,
        description=text,
        fields=[hint_field],
        colour=senko.Colour.error(),
        delete_after=15
    )

async def handle_missing_required_argument(ctx, exc):
    """
    Exception handler for :exc:`~discord.ext.commands.MissingRequiredArgument`.
    
    Informs the user of the missing argument. Displays the command usage and
    help command invocation for the command.
    """
    _ = ctx.locale

    # NOTE: Title of the error message for missing required command arguments.
    title = _("{e:error} Missing Required Argument")
    
    # NOTE: Text of the error message for missing required command arguments.
    text = _("**{user}**, you have forgotten the `{parameter}` parameter.")

    # Get variables
    prefix = ctx.default_prefix
    param_key = f"{ctx.command.locale_id}_parameter_{exc.param.name}"
    param_name = _(param_key)

    # Format strings
    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name, parameter=param_name)
    hint_field = hint_for_command(prefix, ctx.command, _)

    await ctx.embed(
        title=title,
        description=text,
        fields=[hint_field],
        colour=senko.Colour.error(),
        delete_after=15
    )

async def handle_too_many_arguments(ctx, exc):
    """
    Exception handler for :exc:`~discord.ext.commands.TooManyArguments`.

    Informs the user that they added too many arguments. Displays the command
    usage and help command invocation for the command.
    """
    _ = ctx.locale

    # NOTE: Title of the error message for too many command parameters.
    title = _("{e:error} Too Many Arguments")

    # NOTE: Text of the error message for too many command parameters.
    text = _("**{user}**, you have supplied too many parameters for this command.")

    # Get variables
    prefix = ctx.default_prefix

    # Format strings
    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name)
    hint_field = hint_for_command(prefix, ctx.command, _)

    await ctx.embed(
        title=title,
        description=text,
        fields=[hint_field],
        colour=senko.Colour.error(),
        delete_after=15
    )

# Quotation errors

async def handle_unexpected_quote_error(ctx, exc):
    """
    Exception handler for :exc:`~discord.ext.commands.UnexpectedQuoteError`.

    Informs the user that quote marks must not appear inside of unquoted strings.
    """
    _ = ctx.locale

    # NOTE: Title for the error message for unexpected quotation errors.
    title = _("{e:error} Bad Quote")

    # NOTE: Text for the error message for unexpected quotation errors.
    text = _(
        "**{user}**, quote marks must not appear inside of unquoted strings.\n"
        "The conflicting quote mark was `{quote}`."
    )

    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name, quote=exc.quote)

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=10
    )

async def handle_invalid_end_of_quoted_string_error(ctx, exc):
    """
    Exception handler for :exc:`~discord.ext.commands.InvalidEndOfQuotedStringError`.

    Informs the user that closing quotation marks must be followed by nothing or
    a space, but not a character.
    """
    _ = ctx.locale

    # NOTE: Title of the error message for invalid quote errors.
    title = _("{e:error} Invalid Quote")

    # NOTE: Text of the error message for invalid quote errors.
    text = _(
        "**{user}**, quoted strings must be followed by nothing or a space.\n"
        "The conflicting character was `{character}`."
    )

    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name, character=exc.char)

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=10
    )

async def handle_expected_closing_quote_error(ctx, exc):
    """
    Exception handler for :exc:`~discord.ext.commands.ExpectedClosingQuoteError`.
    
    Informs the user that quotes must be closed.
    """
    _ = ctx.locale
    user = discord.utils.escape_markdown(ctx.author.display_name)

    # NOTE: Title of the error message for unclosed quotes in command parameters.
    title = _("{e:error} Unclosed Quote")

    # NOTE: Text of the error message for unclosed quotes in command parameters.
    text = _(
        "**{user}**, quotes must be closed. "
        "The missing quote was `{character}`."
    )

    title = ctx.bot.emotes.format(title)
    text = text.format(user=user, character=exc.close_quote)

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=10
    )
