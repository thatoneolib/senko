import logging
import os
import datetime

import discord
from discord.ext import commands

import senko


class Senko(commands.AutoShardedBot):
    r"""
    The central bot class.

    Inherits from :class:`~discord.ext.commands.AutoShardedBot`.

    Parameters
    ----------
    db: asyncpg.pool.Pool
        An asyncpg database connection pool.
    session: aiohttp.ClientSession
        An aiohttp client session.
    loop: asyncio.AbstractEventLoop
        The event loop to use.
    
    Attributes
    ----------
    db: asyncpg.pool.Pool
        The database connection pool.
    session: aiohttp.ClientSession
        An aiohttp client session.
    locales: senko.Locales
        A pool of loaded locales.
    emotes: senko.Emojis
        The asset library for emojis.
    images: senko.Images
        The asset library for images.
    """
    def __init__(self, db, session, loop):
        
        # Prepare and call the parent constructor.
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            messages=True,
            reactions=True,
        )

        member_cache_flags = discord.MemberCacheFlags.from_intents(intents)
        command_prefix = commands.when_mentioned_or(self.config.prefix)

        super().__init__(
            loop=loop,
            intents=intents,
            member_cache_flags=member_cache_flags,
            command_prefix=command_prefix,
            case_insensitive=True,
            chunk_guilds_at_startup=False,
            guild_subscriptions=False
        )

        # Set general attributes.
        self.log = logging.getLogger("senko.bot")
        self.db = db
        self.session = session
        self.path = os.getcwd()
        self._uptime = datetime.datetime.now(tz=datetime.timezone.utc)
        self._exit_code = 0

        # Locales
        self.locales = senko.Locales(default=self.config.locale)

        locale_dir = os.path.join(self.path, "data", "locales")
        for locale in self.config.locales:
            try:
                self.locales.load(os.path.join(locale_dir, f"{locale}.mo"))
            except Exception as e:
                self.log.exception(f"Could not load locale {locale!r}!", exc_info=e)

        # Emojis
        self.emotes = senko.Emojis()
        self.emotes.load_dir(os.path.join(self.path, "data", "emojis"))

        # Images
        self.images = senko.Images()
        self.images.load_dir(os.path.join(self.path, "data", "images"))

        # Extensions
        for ext in self.config.extensions:
            self.load_extension(f"cogs.{ext}")
        
        self.log.info(f"Loaded {len(self.config.extensions)} extension(s).")

    # Reloading

    def setup_modules(self):
        """
        Set up the internal modules.
        """

    def setup_cogs(self):
        """
        Load all extensions defined in :data:`config.extensions`.
        """
        for ext in self.config.extensions:
            self.load_extension(ext)

    def reload(self):
        """
        Reload the core package and all extensions.
        """


    # Properties

    @property
    def startup_time(self):
        """
        datetime.datetime: An aware utc datetime of when the bot instance was created.
        """
        return self._uptime

    @property
    def uptime(self):
        """
        datetime.timedelta: A timedelta representing the total uptime of the bot.
        """
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        return now - self._uptime

    @property
    def config(self):
        """
        The :ref:`configuration <configuration>` object.
        """
        return __import__("config")

    async def close(self, code=None):
        """
        Close the connection to Discord and shut the bot down.

        Parameters
        ----------
        code: Optional[int]
            An optional :ref:`exit code <exit_codes>` to return.
        """
        if self._closed:
            return

        if code is not None:
            self._exit_code = code

        self.log.info(f"Closing with exit code {self._exit_code}.")

        await self.db.close()
        await self.session.close()
        await super().close()

    def run(self):
        """
        Run the bot using the configured token.

        This method blocks until the bot is terminated.

        Returns
        -------
        int
            The :ref:`exit code <exit_codes>` of the bot.
        """
        super().run(self.config.token)
        return self._exit_code

    def __repr__(self):
        return f"<Senko>"
