import senko
import utils

from .guild import GuildSettings


class SettingsCog(senko.Cog, name="settings"):
    """
    Implements an interface to get and modify settings.
    """

    def __init__(self, bot):
        super().__init__(bot)

        # Caches
        self.guild_cache = utils.caching.LRUCache(512)

    @senko.Cog.listener()
    async def on_guild_join(self, guild):
        # When joining a guild for the first time create a new default
        # configuration. If a configuration already exists, update the
        # last_joined timestamp instead.
        await self._init_guild_settings(guild)

    def _build_guild_settings(self, guild, row):
        """
        Build the :class:`~.GuildSettings` for a guild and database record.

        Parameters
        ----------
        guild: discord.Guild
            The guild to generate the settings object for.
        row: asyncpg.Record
            The database record of the guild's settings.

        Returns
        -------
        ~.GuildSettings
            The guild settings object.
        """
        return GuildSettings(
            self.bot,
            guild,
            prefix=row["prefix"],
            locale=row["locale"],
            timezone=row["timezone"],
            first_joined=row["first_joined"],
            last_joined=row["last_joined"],
        )

    async def _init_guild_settings(self, guild, connection=None):
        """
        Initialize the settings for a guild.

        If settings already exist for the given guild,
        the ``last_joined`` value is updated instead.

        Parameters
        ----------
        guild: discord.Guild
            The guild for which to initialize settings.
        connection: Optional[asyncpg.connection.Connection]
            An optional database connection to use.
        
        Returns
        -------
        ~.GuildSettings
            The new or updated guild settings.
        """

        query = """
        INSERT INTO "guild_settings" ("guild") VALUES ($1)
        ON CONFLICT ("guild") DO UPDATE
        SET "last_joined"=(NOW() AT TIME ZONE 'UTC')
        RETURNING *;
        """
        async with utils.db.maybe_acquire(self.bot.db, connection) as conn:
            row = await conn.fetchrow(query, guild.id)

            # Update cached settings...
            if guild.id in self.guild_cache:
                settings = self.guild_cache[guild.id]
                settings._update(
                    prefix=row["prefix"],
                    locale=row["locale"],
                    timezone=row["timezone"],
                    last_joined=row["last_joined"],
                )

            # ... or cache returned settings.
            else:
                settings = self._build_guild_settings(guild, row)
                self.guild_cache[guild.id] = settings
            
            return settings

    async def get_guild_settings(self, guild, connection=None):
        """
        Get the settings for a guild.

        If no settings exist for the given guild, a new entry is created.

        Parameters
        ----------
        guild: discord.Guild
            The guild to get the settings for.
        connection: Optional[asyncpg.connection.Connection]
            A database connection to use.

        Returns
        -------
        ~cogs.settings.GuildSettings
            The settings object for the guild.
        """
        # Check the cache first.
        if guild.id in self.guild_cache:
            return self.guild_cache[guild.id]

        # Fetch guild settings.
        query = 'SELECT * FROM "guild_settings" WHERE "guild"=$1;'
        async with utils.db.maybe_acquire(self.bot.db, connection) as conn:
            row = await conn.fetchrow(query, guild.id)

            if row is None:
                return await self._init_guild_settings(guild, connection=conn)

        settings = self._build_guild_settings(guild, row)
        self.guild_cache[guild.id] = settings
        return settings
