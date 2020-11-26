.. _cogs_error_handlers:

Error Handlers
##############

The error handler extension implements error handlers for the exceptions raised
by the commands extension of discord.py and the exceptions defined in the bot
core.

The error handlers defined in this extension are automatically added to the
:class:`~senko.Logging` instance found under :attr:`senko.Senko.logging` when
the extension is loaded, and are automatically removed when the extension is
unloaded.

.. note::

    Some handler functions have ``ctx, *args, **kwargs`` as their arguments.
    They still take the same arguments as any other exception handler. The
    difference in arguments is caused by the :class:`~.count_calls` decorator
    that wraps the original handler function to inject the ``calls`` keyword.

Discord.py Handlers
*******************

The extension implements exception handlers for the following types from
``discord.ext.commands``.

=============================================================== ====================================================================
Exception                                                       Handler
=============================================================== ====================================================================
:exc:`~discord.ext.commands.CommandNotFound`                    :func:`~cogs.error_handlers.handlers.handle_command_not_found`
:exc:`~discord.ext.commands.CommandOnCooldown`                  :func:`~cogs.error_handlers.handlers.handle_command_on_cooldown`
:exc:`~discord.ext.commands.DisabledCommand`                    :func:`~cogs.error_handlers.handlers.handle_disabled_command`.

:exc:`~discord.ext.commands.BadArgument`                        :func:`~cogs.error_handlers.handlers.handle_bad_argument`
:exc:`~discord.ext.commands.BadUnionArgument`                   :func:`~cogs.error_handlers.handlers.handle_bad_argument`
:exc:`~discord.ext.commands.MissingRequiredArgument`            :func:`~cogs.error_handlers.handlers.handle_missing_required_argument`
:exc:`~discord.ext.commands.TooManyArguments`                   :func:`~cogs.error_handlers.handlers.handle_too_many_arguments`

:exc:`~discord.ext.commands.UnexpectedQuoteError`               :func:`~cogs.error_handlers.handlers.handle_unexpected_quote_error`
:exc:`~discord.ext.commands.InvalidEndOfQuotedStringError`      :func:`~cogs.error_handlers.handlers.handle_invalid_end_of_quoted_string_error`
:exc:`~discord.ext.commands.ExpectedClosingQuoteError`          :func:`~cogs.error_handlers.handlers.handle_expected_closing_quote_error`

:exc:`~discord.ext.commands.MissingPermissions`                 :func:`~cogs.error_handlers.handlers.handle_missing_permissions`
:exc:`~discord.ext.commands.BotMissingPermissions`              :func:`~cogs.error_handlers.handlers.handle_bot_missing_permissions`
:exc:`~discord.ext.commands.NoPrivateMessages`                  :func:`~cogs.error_handlers.handlers.handle_no_private_message`
:exc:`~discord.ext.commands.PrivateMessageOnly`                 :func:`~cogs.error_handlers.handlers.handle_private_message_only`
:exc:`~discord.ext.commands.NSFWChannelRequired`                :func:`~cogs.error_handlers.handlers.handle_nsfw_channel_required`
:exc:`~discord.ext.commands.NotOwner`                           :func:`~cogs.error_handlers.handlers.handle_not_owner`

:exc:`~discord.ext.commands.ExtensionError`                     :func:`~cogs.error_handlers.handlers.handle_extension_error`
:exc:`~discord.ext.commands.ExtensionAlreadyLoaded`             :func:`~cogs.error_handlers.handlers.handle_extension_error`
:exc:`~discord.ext.commands.ExtensionNotLoaded`                 :func:`~cogs.error_handlers.handlers.handle_extension_error`
:exc:`~discord.ext.commands.NoEntryPointError`                  :func:`~cogs.error_handlers.handlers.handle_extension_error`
:exc:`~discord.ext.commands.ExtensionFailed`                    :func:`~cogs.error_handlers.handlers.handle_extension_error`
:exc:`~discord.ext.commands.ExtensionNotFound`                  :func:`~cogs.error_handlers.handlers.handle_extension_error`
=============================================================== ====================================================================

Invocation Errors
=================

Handlers for exceptions raised during the invocation of a command.

.. autofunction:: cogs.error_handlers.handlers.handle_command_not_found
.. autofunction:: cogs.error_handlers.handlers.handle_command_on_cooldown
.. autofunction:: cogs.error_handlers.handlers.handle_disabled_command

Parameter and Parsing Errors
============================

Handlers for exceptions raised while checking for and parsing parameters.

.. autofunction:: cogs.error_handlers.handlers.handle_bad_argument
.. autofunction:: cogs.error_handlers.handlers.handle_missing_required_argument
.. autofunction:: cogs.error_handlers.handlers.handle_too_many_arguments

Quotation Errors
================

Handlers for exceptions raised while handling quotation characters in parameters.

.. autofunction:: cogs.error_handlers.handlers.handle_unexpected_quote_error
.. autofunction:: cogs.error_handlers.handlers.handle_invalid_end_of_quoted_string_error
.. autofunction:: cogs.error_handlers.handlers.handle_expected_closing_quote_error

Check Errors
============

Handlers for exceptions raised in command checks native to ``discord.ext.commands``.

.. autofunction:: cogs.error_handlers.handlers.handle_missing_permissions
.. autofunction:: cogs.error_handlers.handlers.handle_bot_missing_permissions
.. autofunction:: cogs.error_handlers.handlers.handle_no_private_message
.. autofunction:: cogs.error_handlers.handlers.handle_private_message_only
.. autofunction:: cogs.error_handlers.handlers.handle_nsfw_channel_required
.. autofunction:: cogs.error_handlers.handlers.handle_not_owner

Extension Errors
================

Handlers for exceptions raised when loading or unloading extensions.

.. autofunction:: cogs.error_handlers.handlers.handle_extension_error

Custom Handlers
***************

The extension further implements exception handlers for the following custom
exception types.

.. todo:: Document custom exception handlers.

Helpers
*******

.. autofunction:: cogs.error_handlers.helpers.usage_for_command
.. autofunction:: cogs.error_handlers.helpers.help_invocation_for_command
.. autofunction:: cogs.error_handlers.helpers.hint_for_command

The :class:`~.count_calls` decorator class lets us prevent spammy
error messages by counting how many times an error handler has been
called within a given timeframe. This is particularly useful for
exceptions that should naturally deter users from reusing the command
for some time, such as :class:`~discord.ext.commands.CommandOnCooldown`
or :class:`~discord.ext.commands.DisabledCommand`.

.. autoclass:: cogs.error_handlers.helpers.count_calls