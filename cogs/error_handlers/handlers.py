import datetime
import io
import traceback

import discord
import senko
import utils
from babel.dates import format_timedelta
from discord.ext import commands

from .helpers import count_calls, hint_for_command, format_permissions

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

    # Check errors
    "handle_missing_permissions",
    "handle_bot_missing_permissions",
    "handle_no_private_message",
    "handle_private_message_only",
    "handle_nsfw_channel_required",
    "handle_not_owner",

    # Extension errors
    "handle_extension_error",
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
        delete_after=15,
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
        delete_after=15,
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
        delete_after=15
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
        delete_after=15
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
        delete_after=15
    )


# Check errors

@count_calls(10, commands.BucketType.member)
async def handle_missing_permissions(ctx, exc, calls=0):
    """
    Exception handler for :exc:`~discord.ext.commands.MissingPermissions`.

    Informs the user of the permissions they are missing to run the command.
    
    Has a cooldown of 10 seconds per member.
    """
    if calls > 0:
        return
        
    _ = ctx.locale

    # NOTE: Title of the error message for missing permissions.
    title = _("{e:error} Missing Permissions")

    # NOTE: Text of the error message for missing permissions.
    # NOTE: 'permissions' is a formatted list of permissions of varying length.
    # NOTE: Examples: 'manage channels', 'manage channels and manage messages'
    text = _(
        "**{user}**, you are missing the following permissions to "
        "use `{command}`: {permissions}."
    )

    # Format text
    permissions = format_permissions(exc.missing_perms, _)
    command = ctx.command.get_qualified_name(_)
    title = ctx.bot.emotes.format(title)
    text = text.format(
        user=ctx.display_name, 
        command=command, 
        permissions=permissions
    )

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=15
    )

@count_calls(10, commands.BucketType.member)
async def handle_bot_missing_permissions(ctx, exc, calls=0):
    """
    Exception handler for :exc:`~discord.ext.commands.BotMissingPermissions`.

    Informs the user of the permissions the bot is missing to run the command.
    
    Has a cooldown of 10 seconds per member.
    """
    if calls > 0:
        return
        
    _ = ctx.locale

    # NOTE: Title of the error message for missing bot permissions.
    title = _("{e:error} Bot Missing Permissions")

    # NOTE: Text of the error message for missing bot permissions.
    # NOTE: 'permissions' is a formatted list of permissions of varying length.
    # NOTE: Examples: 'manage channels', 'manage channels and manage messages'
    text = _(
        "**{user}**, I am missing the following permissions to "
        "run `{command}`: {permissions}."
    )

    # Format text
    permissions = format_permissions(exc.missing_perms, _)
    command = ctx.command.get_qualified_name(_)
    title = ctx.bot.emotes.format(title)
    text = text.format(
        user=ctx.display_name, 
        command=command, 
        permissions=permissions
    )

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=15
    )

@count_calls(10, commands.BucketType.user)
async def handle_no_private_message(ctx, exc, calls=0):
    """
    Exception handler for :exc:`~discord.ext.commands.NoPrivateMessage`.

    Informs the user that the command can not be used in private messages.
    
    Has a cooldown of 10 seconds per user.
    """
    if calls > 0:
        return

    _ = ctx.locale

    # NOTE: Title of the error message for commands that can not be used in DMs.
    title = _("{e:error} No Private Messages")

    # NOTE: Text of the error message for commands that can not be used in DMs.
    text = _(
        "**{user}**, the `{command}` command can not be used in "
        "private messages."
    )

    command = ctx.command.get_qualified_name(_)

    # Format text
    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name, command=command)

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=15
    )

@count_calls(10, commands.BucketType.user)
async def handle_private_message_only(ctx, exc, calls=0):
    """
    Exception handler for :exc:`~discord.ext.commands.PrivateMessageOnly`.

    Informs the user that the command can only be used in private messages.
    
    Has a cooldown of 10 seconds per user.
    """
    if calls > 0:
        return
        
    _ = ctx.locale

    # NOTE: Title of the error message for commands that can only be used in DMs.
    title = _("{e:error} Private Messages Only")

    # NOTE: Text of the error message for commands that can only be used in DMs.
    text = _(
        "**{user}**, the `{command}` command can only be used in "
        "private messages."
    )

    command = ctx.command.get_qualified_name(_)

    # Format text
    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name, command=command)

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=15
    )

@count_calls(10, commands.BucketType.user)
async def handle_nsfw_channel_required(ctx, exc, calls=0):
    """
    Exception handler for :exc:`~discord.ext.commands.NSFWChannelRequired`.

    Informs the user that the command can only be used in NSFW channels.
    
    Has a cooldown of 10 seconds per user.
    """
    if calls > 0:
        return
        
    _ = ctx.locale

    # NOTE: Title of the error message for commands that can only be used in NSFW channels.
    title = _(":underage: NSFW Channel Required")

    # NOTE: Text of the error message for commands that can only be used in NSFW channels.
    text = _("**{user}**, the `{command}` command can only be used in NSFW channels.")

    command = ctx.command.get_qualified_name(_)

    # Format text
    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name, command=command)

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=15
    )

@count_calls(10, commands.BucketType.user)
async def handle_not_owner(ctx, exc, calls=0):
    """
    Exception handler for :exc:`~discord.ext.commands.NotOwner`.

    Informs the user that the command can only be used by an owner.

    Has a cooldown of 10 seconds per user.
    """
    if calls > 0:
        return
        
    _ = ctx.locale

    # NOTE: Title of the error message for commands that can only be used by an owner.
    title = _(":no_entry_sign: Owner Only")

    # NOTE: Text of the error message for commands that can only be used by an owner.
    text = _("**{user}**, the `{command}` command can only be used by the owner.")

    command = ctx.command.get_qualified_name(_)

    # Format text
    title = ctx.bot.emotes.format(title)
    text = text.format(user=ctx.display_name, command=command)

    await ctx.embed(
        title=title,
        description=text,
        colour=senko.Colour.error(),
        delete_after=15
    )

# Extension errors

async def handle_extension_error(ctx, exc):
    """
    Exception handler for :exc:`~discord.ext.commands.ExtensionError` and
    its derived exception types.

    As this is a handler for a more technical exception it does not support
    localization.

    Informs the user of the exception and attaches the traceback for
    :exc:`~discord.ext.commands.ExtensionFailed`.
    
    The messages sent by this handler are not translated as they will
    never appear for regular users.
    """
    extra = dict()
    title = ":gear: Extension Error"

    if isinstance(exc, commands.ExtensionAlreadyLoaded):
        text = "**{user}**, the `{extension}` extension is already loaded."
    elif isinstance(exc, commands.ExtensionNotLoaded):
        text = "**{user}**, the `{extension}` extension is not loaded."
    elif isinstance(exc, commands.NoEntryPointError):
        text = "**{user}**, the `{extension}` extension does not have a setup function."
    elif isinstance(exc, commands.ExtensionNotFound):
        text = "**{user}**, the `{extension}` extension could not be found."
    elif isinstance(exc, commands.ExtensionFailed):
        text = "**{user}**, the `{extension}` extension could not be loaded due to an error."

        original = exc.original
        trace = "".join(traceback.format_exception(type(original), original, original.__traceback__))

        if len(trace) > 1000:
            display = f"```\n{trace[:990]}...```"
            buffer = io.BytesIO(trace.encode("utf-8"))
            extra["file"] = discord.File(buffer, f"traceback.txt")
        else:
            display = f"```\n{trace}```"

        extra["fields"] = [dict(name="Traceback", value=display)]

    text = text.format(user=ctx.display_name, extension=exc.name)
    await ctx.embed(title=title, description=text, colour=senko.Colour.error(), **extra)
