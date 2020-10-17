.. _bot:

Bot
###

The bot class is a :class:`~discord.ext.commands.AutoShardedBot` with a set of
modifications made to it that enable advanced behavior.

Modifications
*************

* The ``command_prefix`` defaults to the :data:`config.prefix` or a mention.
* The ``case_insensitive`` parameter is set to ``true`` by default.
* The database connection pool is exposed as :attr:`senko.Senko.db`.
* The client session is exposed as :attr:`senko.Senko.session`.
* The :ref:`configuration` is exposed as :attr:`senko.Senko.config`.
* The :func:`~senko.Senko.close` method now takes an optional ``code`` parameter
  to set the exit code returned by :func:`~senko.Senko.run`.
* The :func:`senko.Senko.run` method no longer takes a ``token`` parameter.

Reference
*********

.. autoclass:: senko.Senko
    :members:
