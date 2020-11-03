.. _core_command:

Command and Group
#################

To enable some special behavior required by the bot, Senko comes with a modified
commands framework based on ``discord.ext.command``. For the most part, the
objects created using the custom command and group classes still behave the
same as their parents. The major changes are for convenience and to support
localization.

Key Changes
***********

The following changes have been made:

* The default converters for primitives and discord models are now taken from ``senko.converters`` (see :ref:`core_converters`).
* The :attr:`~senko.command.overrides.CommandOverrides.locale_id` attribute has been added.
* Various ``get_`` methods have been added that allow access to localized variants of otherwise untranslatable attributes.

Decorators
**********

These decorators are analogue to :func:`~discord.ext.commands.command` and
:func:`~discord.ext.commands.group`, but create :class:`senko.Command` and
:class:`senko.Group` commands by default.

.. autofunction:: senko.command
.. autofunction:: senko.group

Command
*******

.. autoclass:: senko.Command
    :members:

Group
*****

.. autoclass:: senko.Group
    :members:

Overrides
*********

.. autoclass:: senko.command.overrides.CommandOverrides
    :members:
