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

.. data:: config.timezone
    :type: str
    :value: "utc"

    The default timezone for guilds and users.

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

.. data:: config.logging_webhook
    :type: Optional[str]
    :value: ...

    An optional URL of a Discord webhook. When specified, unhandled command
    errors and log messages of logging domains specified in
    :data:`config.logging_domains` are sent through this webhook.

.. data:: config.logging_domains
    :type: List[Tuple[str, int]]
    :value: [("senko", 20)]

    A list of logging domains and logging levels. Any log records emitted
    by the corresponding domain whose level is equal or higher to the one
    specified will be sent through the logging webhook.

.. data:: config.debug
    :type: bool
    :value: False

    Toggles debug mode. Enables more verbose logging, disables certain features
    that should not be active when not in production and enables additional
    functionality for debugging. This should not be enabled in production.

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

    # The default timezone to use for users and guilds.
    timezone = "utc"

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

    # The webhook through which unhandled command errors and the log messages from
    # the domains defined in logging_domains are logged.
    logging_webhook = "WEBHOOK URL"

    # Logging domains and their default log levels.
    # Levels: CRITICAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10
    logging_domains = [("senko", 20)]

    # Toggles debug mode. Enables more verbose logging, disables certain features
    # that should not be active when not in production and enables additional
    # functionality for debugging. This should not be enabled in production.
    debug = False