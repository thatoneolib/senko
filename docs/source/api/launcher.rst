.. _launcher:

Launcher
########

.. _uvloop: https://github.com/MagicStack/uvloop

Senko comes with a launcher that takes care of the initial setup. During this
setup the launcher performs the following steps:

* Select an event loop appropriate for the operating system.

    * On Linux: When installed, `uvloop`_ is used for the event loop.
    * On Windows: The default event loop (:class:`asyncio.ProactorEventLoop`) is used.

* Prepare the :py:mod:`logging` module.
* Create a :class:`asyncpg.pool.Pool` connected to the database.
* Create an :class:`aiohttp.ClientSession`.
* Load all extensions listed in :data:`config.extensions`.
* Run the bot.

The launcher can be started by either executing the ``launch.py`` file directly,
or through the ``launch.sh`` script, which will also handle the special case of
the :ref:`exit code <exit_codes>` 25.

.. _exit_codes:

Exit Codes
**********

Upon closing, the launcher returns one of four exit codes that indicate why the
bot stopped and how to proceed. The table below lists each exit code and its
respective meaning.

======= ========================================================================
Code    Meaning
======= ========================================================================
0       Regular exit.
1       An error occured.
25      Pull from git remote and restart the bot.
26      Restart the bot.
======= ========================================================================
