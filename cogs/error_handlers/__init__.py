from . import handlers
import discord
from discord.ext import commands

# Exception handlers

HANDLERS = {
    commands.CommandNotFound: handlers.handle_command_not_found,
    commands.CommandOnCooldown: handlers.handle_command_on_cooldown,
    commands.DisabledCommand: handlers.handle_disabled_command,
}

# Extension methods

def setup(bot):
    for exception, handler in HANDLERS.items():
        bot.logging.add_handler(exception, handler)


def teardown(bot):
    for exception in HANDLERS.keys():
        bot.logging.remove_handler(exception)