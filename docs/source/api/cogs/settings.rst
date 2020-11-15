.. _cogs_settings:

Settings
########

The settings cog provides access to guild and user settings and allows them to
be modified through the use of database models.

Usage
*****

You can access the loaded settings cog either through :attr:`.Senko.settings`
or by calling :meth:`.Senko.get_cog` with its qualified name.

Guild Settings
==============

.. code-block:: python3

    settings = await self.bot.settings.get_guild_settings(ctx.guild)

    # settings.guild
    # settings.prefix
    # settings.locale
    # settings.timezone
    # settings.first_joined
    # settings.last_joined

    await settings.update(prefix="?", locale="de_DE", ...)

User Settings
=============

.. todo:: Add an example for accessing user settings.

Cog
***

The qualified name of the :class:`~cogs.settings.SettingsCog` is ``settings``.
When loaded, you can access this cog through :attr:`.Senko.settings`.

.. autoclass:: cogs.settings.SettingsCog
    :members:

Models
******

To make working with them easier, settings are provided as models. You receive
an instance of these when calling the appropriate method of the settings cog.

Guild Settings
==============

The guild settings database model represents an entry in the ``guild_settings``
table in the database.

.. autoclass:: cogs.settings.GuildSettings
    :members:

User Settings
==============

.. todo:: Document user settings.

Exceptions
**********

The following exceptions may be raised by :class:`~cogs.settings.SettingsCog`:

.. autoexception:: cogs.settings.UnknownSetting

.. autoexception:: cogs.settings.BadSetting
