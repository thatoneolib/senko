.. _core_bot:

Bot
###

The bot class is a :class:`~discord.ext.commands.AutoShardedBot` with a set of
modifications made to it that enable advanced behavior.

Modifications
*************

* The ``intents`` parameter it set to the following :class:`discord.Intents`
  confguration. The member cache flags are generated accordingly.

  .. code-block::

      intents = discord.Intents(
          guilds=True,
          members=True,
          bans=True,
          emojis=True,
          messages=True,
          reactions=True,
      )

* The ``command_prefix`` parameter is set to :func:`senko.command_prefix`.
* The ``case_insensitive`` parameter is set to ``True``.
* The ``chunk_at_startup`` parameter is set to ``False``.
* The ``guild_subscriptions`` parameter is set to ``False``.
* The database connection pool is exposed as :attr:`senko.Senko.db`.
* The client session is exposed as :attr:`senko.Senko.session`.
* The :ref:`configuration` is exposed as :attr:`senko.Senko.config`.
* The :func:`~senko.Senko.close` method now takes an optional ``code`` parameter
  to set the exit code returned by :func:`~senko.Senko.run`.
* The :func:`senko.Senko.run` method no longer takes a ``token`` parameter.
* Added commands without a cooldown receive a cooldown of 3 seconds per user.
* The 3 second cooldown is also applied to children of added command groups.
* Added cogs must be of :class:`senko.Cog`, or a :exc:`TypeError` will be raised.
* Added commands must be of :class:`senko.Command` or :class:`senko.Group`, or a :exc:`TypeError` will be raised.

Reference
*********

.. autofunction:: senko.command_prefix

.. autoclass:: senko.Senko
    :members:
