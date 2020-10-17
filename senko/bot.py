import logging

from discord.ext import commands


class Senko(commands.AutoShardedBot):
    r"""
    The central bot class.

    Inherits from :class:`~discord.ext.commands.AutoShardedBot`.

    Parameters
    ----------
    \*args
        Positional arguments to pass on to the parent class.
    db: asyncpg.pool.Pool
        An asyncpg database connection pool.
    session: aiohttp.ClientSession
        An aiohttp client session.
    \*\*kwargs
        Keyword arguments to pass on to the parent class.
    """

    def __init__(self, *args, db=None, session=None, **kwargs):
        # Default parameters
        command_prefix = kwargs.pop("command_prefix", None)
        if command_prefix is None:
            command_prefix = commands.when_mentioned_or(self.config.prefix)

        case_insensitive = kwargs.pop("case_insensitive", None)
        if case_insensitive is None:
            case_insensitive = True

        super().__init__(
            *args,
            command_prefix=command_prefix,
            case_insensitive=case_insensitive,
            **kwargs,
        )

        # Attributes
        self.log = logging.getLogger("senko.bot")
        self._db = db
        self._session = session
        self._exit_code = 0

    @property
    def db(self):
        """
        asyncpg.pool.Pool: The database connection pool.
        """
        return self._db

    @property
    def session(self):
        """
        aiohttp.ClientSession: An aiohttp client session.
        """
        return self._session

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
