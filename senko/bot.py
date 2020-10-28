import logging
import os

import discord
from discord.ext import commands

from .i18n import Locales


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

    Attributes
    ----------
    db: asyncpg.pool.Pool
        The database connection pool.
    session: aiohttp.ClientSession
        An aiohttp client session.
    locales: senko.Locales
        A pool of loaded locales.
    """
    def __init__(self, db, session):
        
        # Prepare and call the parent constructor.
        intents = discord.Intents.all()
        intents.presences = False # Requires verification.
        intents.integrations = False
        intents.webhooks = False
        intents.invites = False
        intents.voice_states = False
        intents.typing = False
        
        member_cache_flags = discord.MemberCacheFlags.from_intents(intents)
        command_prefix = commands.when_mentioned_or(self.config.prefix)

        super().__init__(
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
        
        self._exit_code = 0

        # Interfaces
        self.locales = Locales(default=self.config.locale)

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
