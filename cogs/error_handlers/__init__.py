from . import handlers
import discord
import logging
from discord.ext import commands

# Exception handlers

HANDLERS = {
    # Invocation errors
    commands.CommandNotFound: handlers.handle_command_not_found,
    commands.CommandOnCooldown: handlers.handle_command_on_cooldown,
    commands.DisabledCommand: handlers.handle_disabled_command,
    
    # Parameter and parsing errors
    commands.BadArgument: handlers.handle_bad_argument,
    commands.BadUnionArgument: handlers.handle_bad_argument,
    commands.MissingRequiredArgument: handlers.handle_missing_required_argument,
    commands.TooManyArguments: handlers.handle_too_many_arguments,
    
    # Quotation errors
    commands.UnexpectedQuoteError: handlers.handle_unexpected_quote_error,
    commands.InvalidEndOfQuotedStringError: handlers.handle_invalid_end_of_quoted_string_error,
    commands.ExpectedClosingQuoteError: handlers.handle_expected_closing_quote_error,
    
    # Check errors
    commands.MissingPermissions: handlers.handle_missing_permissions,
    commands.BotMissingPermissions: handlers.handle_bot_missing_permissions,
    commands.NoPrivateMessage: handlers.handle_no_private_message,
    commands.PrivateMessageOnly: handlers.handle_private_message_only,
    commands.NSFWChannelRequired: handlers.handle_nsfw_channel_required,
    commands.NotOwner: handlers.handle_not_owner,

    # Extension errors
    commands.ExtensionError: handlers.handle_extension_error,
    commands.ExtensionAlreadyLoaded: handlers.handle_extension_error,
    commands.ExtensionNotLoaded: handlers.handle_extension_error,
    commands.NoEntryPointError: handlers.handle_extension_error,
    commands.ExtensionFailed: handlers.handle_extension_error,
    commands.ExtensionNotFound: handlers.handle_extension_error,
}

# Extension methods

def setup(bot):
    for exception, handler in HANDLERS.items():
        bot.logging.add_handler(exception, handler)

    log = logging.getLogger("cogs.error_handlers")
    log.info(f"Registered {len(HANDLERS)} exception handler(s).")

def teardown(bot):
    for exception in HANDLERS.keys():
        bot.logging.remove_handler(exception)

    log = logging.getLogger("cogs.error_handlers")
    log.info(f"Unregistered {len(HANDLERS)} exception handler(s).")
