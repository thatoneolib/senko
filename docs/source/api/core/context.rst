.. _core_context:

Context
#######

The modified command framework comes with two custom context implementations
that extend the default :class:`discord.ext.commands.Context` with additional
properties and methods that simply common use cases such as fetching the default
command prefix for a context, the display name of the context author or sending
an embed.

Command Context
***************

This context directly inherits from :class:`discord.ext.commands.Context` and
extends it with additional properties and methods. It is a superset of the
default context.

This context type is available through :meth:`senko.Senko.get_context`.

.. autoclass:: senko.CommandContext
    :members:

Partial Context
***************

This context inherits from :class:`senko.Context` and is used when you need a
context for a user that is not the original user of a command, e.g. when sending
a prompt to another user using one of the utilities.

This context type is available through :meth:`senko.Senko.get_partial_context`.

.. autoclass:: senko.PartialContext
    :members: