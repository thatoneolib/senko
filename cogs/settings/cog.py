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
        """
        When joining a guild for the first time, creates a new default
        configuration for the guild. If a configuration already exists
        for the joined guild, the ``last_joined`` value is updated to
        the current time.
        """
        await self.new_guild_settings(guild)

    async def new_guild_settings(self, guild, connection=None):
        """
        Create default settings for a guild.

        Updates ``last_joined`` to the current time when
        settings already exist for the given guild.

        Parameters
        ----------
        guild: discord.Guild
            The guild to create new settings for.
        connection: Optional[asyncpg.connection.Connection]
            A database connection to use.
        """
        query = """
        INSERT INTO "guild_settings" ("guild") VALUES ($1)
        ON CONFLICT ("guild") DO UPDATE
        SET "last_joined"=(NOW() AT TIME ZONE 'UTC');
        """

        async with utils.db.maybe_acquire(self.bot.db, connection) as conn:
            await conn.execute(query, guild.id)

            # Sync cached settings.
            if guild.id in self.guild_cache:
                await self.guild_cache[guild.id].sync()

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

        # Fetch the guild settings.
        query = 'SELECT * FROM "guild_settings" WHERE "guild"=$1;'
        async with utils.db.maybe_acquire(self.bot.db, connection) as conn:
            row = await conn.fetchrow(query, guild.id)

            if row is None:
                await self.new_guild_settings(guild, connection=conn)
                row = await conn.fetchrow(query, guild.id)

            settings = GuildSettings(
                self.bot,
                guild,
                prefix=row["prefix"],
                locale=row["locale"],
                timezone=row["timezone"],
                first_joined=row["first_joined"],
                last_joined=row["last_joined"],
            )

        # Cache settings and return.
        self.guild_cache[guild.id] = settings
        return settings
