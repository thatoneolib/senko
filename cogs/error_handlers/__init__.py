from . import handlers
import discord
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
}

# Extension methods

def setup(bot):
    for exception, handler in HANDLERS.items():
        bot.logging.add_handler(exception, handler)


def teardown(bot):
    for exception in HANDLERS.keys():
        bot.logging.remove_handler(exception)
