.. _cogs_settings:

Settings
########

The settings cog maintains and provides access to settings. It provides an
interface to retrieve settings objects through which you can access and modify
settings for guilds and users.

Usage
*****

The loaded settings cog can be accessed through :attr:`.Senko.settings` or by
calling :meth:`.Senko.get_cog` with its qualified name.

Guild Settings
==============

You can access the settings for a guild as follows:

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
A shortcut to the loaded cog exists under :attr:`.Senko.settings`.

.. autoclass:: cogs.settings.SettingsCog
    :members:

Models
******

Guild and user settings are provided as models. Instances of these models are
returned by the corresponding methods of the settings cog.

Guild Settings
==============

The model for guild settings represents a single row in the ``guild_settings``
table. Instances of this class are available through :meth:`.SettingsCog.get_guild_settings`.

.. autoclass:: cogs.settings.GuildSettings
    :members:

User Settings
==============

.. todo:: Document user settings.

Exceptions
**********

When modifying the settings for a guild or user the following exceptions may
be raised:

.. autoexception:: cogs.settings.UnknownSetting

.. autoexception:: cogs.settings.BadSetting
