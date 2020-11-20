import utils
import zoneinfo

from .errors import BadSetting, UnknownSetting


class GuildSettings(object):
    """
    A database model that represents the settings for a guild.

    You should not create this yourself and instead get instances
    of this class through :meth:`~cogs.settings.SettingsCog.get_guild_settings`.
    """

    __slots__ = (
        "_bot",
        "_guild",
        "_prefix",
        "_locale",
        "_timezone",
        "_first_joined",
        "_last_joined",
    )

    def __init__(self, bot, guild, **options):
        self._bot = bot
        self._guild = guild
        self._prefix = options.pop("prefix")
        self._locale = options.pop("locale")
        self._timezone = options.pop("timezone")
        self._first_joined = options.pop("first_joined")
        self._last_joined = options.pop("last_joined")

    @property
    def guild(self):
        """discord.Guild: The guild these settings are for."""
        return self._guild

    @property
    def prefix(self):
        """str: The guild prefix. If no guild prefix has been set, this
        returns :data:`config.prefix` instead."""
        return self._prefix or self._bot.config.prefix

    @property
    def locale(self):
        """str: The ID of the guild locale. If no guild locale has been set,
        this returns :data:`config.locale` instead."""
        return self._locale or self._bot.config.locale

    @property
    def timezone(self):
        """str: The name of the guild timezone. If no guild timezone has been
        set, this returns :data:`config.timezone` instead."""
        return self._timezone or self._bot.config.timezone

    @property
    def first_joined(self):
        """datetime.datetime: The datetime when the bot first joined the guild."""
        return self._first_joined

    @property
    def last_joined(self):
        """datetime.datetime: The datetime when the bot last joined the guild."""
        return self._last_joined

    def _update(self, **options):
        r"""
        Update the settings object.

        Parameters
        ----------
        \*\*options
            The fields to update.
        """
        valid = ("prefix", "locale", "timezone", "last_joined")

        for option, value in options.items():
            if option not in valid:
                raise TypeError(f"Received unexpected field: {option!r}!")

            setattr(self, f"_{option}", value)

    async def update(self, connection=None, **options):
        """
        Update the guild settings.

        Parameters
        ----------
        connection: Optional[asyncpg.connection.Connection]
            A database connection to use.
        prefix: Optional[str]
            The new guild prefix. Can be ``None`` to reset the guild
            prefix to the default prefix.
        locale: Optional[str]
            The new guild locale. Can be ``None`` to reset the guild
            locale to the default locale.
        timezone: Optional[str]
            The new timezone. Can be ``None`` to reset the guild
            timezone to the default timezone.
        last_joined: Optional[datetime.datetime]
            The new last_joined date.

        Raises
        ------
        BadSetting
            When an invalid value is provided for an option.
        UnknownSetting
            When an invalid guild setting is provided.
        """
        if not options:
            return

        # Validate the provided options.
        valid = ("prefix", "locale", "timezone", "last_joined")

        for option, value in options.items():
            if option not in valid:
                raise UnknownSetting(f"Unknown guild setting: {option!r}")

            if option == "prefix" and value is not None:
                if len(value) == 0:
                    raise BadSetting("Guild prefix must not be empty!")
                elif len(value) > 10:
                    raise BadSetting("Guild prefix must be at most 10 characters long!")

            # TODO: Validate timezone.

        # Build the database query.
        skeleton = 'UPDATE "guild_settings"SET {assignments} WHERE "guild"=$1;'
        enumerated = list(enumerate(options.items(), 2))
        assignments = ", ".join(f'"{pair[0]}"=${pos}' for pos, pair in enumerated)
        values = [pair[1] for _, pair in enumerated]
        query = skeleton.format(assignments=assignments)

        async with utils.db.maybe_acquire(self._bot.db, connection) as db:
            await db.execute(query, self._guild.id, *values)

        # Update the model.
        self._update(**options)

    def __repr__(self):
        return f"<GuildSettings guild={self._guild} prefix={self._prefix!r} locale={self._locale!r} timezone={self._timezone!r}>"
