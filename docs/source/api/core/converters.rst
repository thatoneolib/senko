.. _core_converters:

Converters
##########

The custom command framework used by the bot uses a set of custom converters
that enable the exception handling system to provide localized error messages.

All converters raise either :exc:`~discord.ext.commands.BadArgument` or a
different exception that inherits from :exc:`~discord.ext.commands.CommandError`.

The following categories of converters exist:

=============================== ============================================================
Type                            Description
=============================== ============================================================
:ref:`converters_primitives`    Converters for primitive types such as :class:`int`.
:ref:`converters_discord`       Converters for discord models such as :class:`discord.User`.
=============================== ============================================================

.. _converters_primitives:

Primitives
**********

These converters are injected into the custom command and group classes used by
the bot instead of the default conversion in the ``_actual_conversion`` method.

=================================== ============================================
Type                                Converter
=================================== ============================================
:class:`bool`                       :class:`senko.converters.Bool`
:class:`int`                        :class:`senko.converters.Int`
:class:`float`                      :class:`senko.converters.Float`
=================================== ============================================

.. autoclass:: senko.converters.Bool
.. autoclass:: senko.converters.Int
.. autoclass:: senko.converters.Float

.. _converters_discord:

Discord Models
**************

In addition to new converters for primitives, the set of custom converters also
includes new converters for discord.py's models. These wrap around the existing
converters and always raise :exc:`~discord.ext.commands.BadArgument`.  This is
mostly due to exception handling.

.. note::

    The reason why conversion errors are handled this way instead of handling the
    specialized :exc:`~discord.ext.commands.BadArgument`-derived exceptions is
    because they are sometimes ambiguous. For instance, converting to a
    :class:`discord.Message` may raise :exc:`discord.ext.commands.ChannelNotFound`.
    This exception can also be raised by the :class:`discord.TextChannel` converter.

    To remove this possible ambiguity, we use custom converters.

=================================== ============================================
Type                                Converter
=================================== ============================================
:class:`discord.User`               :class:`senko.converters.User`
:class:`discord.Member`             :class:`senko.converters.Member`
:class:`discord.Message`            :class:`senko.converters.Message`
:class:`discord.TextChannel`        :class:`senko.converters.TextChannel`
:class:`discord.VoiceChannel`       :class:`senko.converters.VoiceChannel`
:class:`discord.CategoryChannel`    :class:`senko.converters.CategoryChannel`
:class:`discord.Invite`             :class:`senko.converters.Invite`
:class:`discord.Role`               :class:`senko.converters.Role`
:class:`discord.Colour`             :class:`senko.converters.Colour`
:class:`discord.Emoji`              :class:`senko.converters.Emoji`
:class:`discord.PartialEmoji`       :class:`senko.converters.PartialEmoji`
=================================== ============================================

.. autoclass:: senko.converters.User
.. autoclass:: senko.converters.Member
.. autoclass:: senko.converters.Message
.. autoclass:: senko.converters.TextChannel
.. autoclass:: senko.converters.VoiceChannel
.. autoclass:: senko.converters.CategoryChannel
.. autoclass:: senko.converters.Invite
.. autoclass:: senko.converters.Role
.. autoclass:: senko.converters.Colour
.. autoclass:: senko.converters.Emoji
.. autoclass:: senko.converters.PartialEmoji