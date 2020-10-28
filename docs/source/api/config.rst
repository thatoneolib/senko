.. _configuration:

Configuration
#############

Senko comes with a central configuration file that contains all of the bot's
settings. All configuration fields and their valid values are documented below.
Finally, you can find a template that can be copied and pasted into a
``config.py`` file at the bottom of this page.

Fields
******

.. data:: config.token
    :type: str
    :value: ""

    The application token of the bot. You can find this on the page of your
    application at https://discordapp.com/developers/applications/me.

.. data:: config.prefix
    :type: str
    :value: "sen!"

    The default command prefix. The bot can also be mentioned instead.

.. data:: config.locales
    :type: List[str]
    :value: ["en_GB"]

    IDs of locales to be loaded from ``/data/locales/`` during setup.

.. data:: config.locale
    :type: str
    :value: "en_GB"

    The default locale of the bot. Must be a value from :data:`config.locales`.

.. data:: config.extensions
    :type: List[str]
    :value: ["introduction", "permissions", "metrics", ...]

    A list of extensions to load from ``/cogs/`` during setup.
    
.. data:: config.database_credentials
    :type: Dict[str, str]
    :value: ...

    The credentials for the PostgreSQL database.

    =============== ===========================================================
    Field           Description
    =============== ===========================================================
    ``user``        The name of the database user to connect with.
    ``password``    The password of the database user to connect with.
    ``host``        The host address on which the database server is running.
    ``port``        The port under which the database server is running.
    ``database``    The name of the database to connect to.
    =============== ===========================================================

.. data:: config.logging_levels
    :type: List[Tuple[str, int]]
    :value: [("senko", 20)]

    A list of logging domains mapped to the logging level that should be set
    for them when the launcher is setting up the logging module.

Template
********

Below you can find a template to create your own ``config.py``.

.. code-block:: python3

    # Senko Configuration File
    #
    # This is the central configuration file for Senko. You can learn more about
    # the contents of this file in the configuration section of the documentation.
    # Alternatively, simply refer to the comments in this file.

    # The application token of the bot. You can find this on the page of
    # your application at https://discordapp.com/developers/applications/me.
    token = "YOUR BOT TOKEN"

    # The default command prefix.
    prefix = "sen!"

    # The languages to load from /data/locales during the setup.
    locales = ["en_GB"]

    # The default language to use. This should be a value from the list above.
    locale = "en_GB"

    # A list of extensions to load from /cogs during the setup.
    extensions = ["extension1", "extension2", "extension3"]

    # The credentials for the PostgreSQL database.
    database_credentials = dict(
        user     = "USERNAME",
        password = "PASSWORD",
        host     = "ADDRESS",
        port     = "PORT",
        database = "DATABASE",
    )

    # Logging domains and their default log levels.
    # Levels: CRITICAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10
    logging_levels = [("senko", 10)]