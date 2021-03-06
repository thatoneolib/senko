import logging
import os
import datetime

import discord
from discord.ext import commands

import senko


async def command_prefix(bot, msg):
    """
    A callable command prefix.

    If possible, uses the :class:`~cogs.settings.SettingsCog` to
    get the command prefix for guilds.

    Allows the bot to be mentioned instead of using the prefix.
    """
    prefix = None
    cog = bot.get_cog("settings")
    if msg.guild and cog:
        settings = await cog.get_guild_settings(msg.guild)
        prefix = settings.prefix

    if prefix is None:
        prefix = bot.config.prefix

    return commands.when_mentioned_or(prefix)(bot, msg)


class Senko(senko.LocaleMixin, commands.AutoShardedBot):
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
    logging: senko.Logging
        The internal logging module.
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

        super().__init__(
            loop=loop,
            intents=intents,
            member_cache_flags=member_cache_flags,
            command_prefix=command_prefix,
            case_insensitive=True,
            chunk_guilds_at_startup=False,
            guild_subscriptions=False,
            help_command=None,
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
        self.set_locale_source(self.locales)

        locale_dir = os.path.join(self.path, "data", "locales")
        for locale in self.config.locales:
            try:
                self.locales.load(os.path.join(locale_dir, f"{locale}.mo"))
            except Exception as e:
                self.log.exception(f"Could not load locale {locale!r}!", exc_info=e)

        # Cog name mapping. Maps locale IDs to dicts of cog name translations.
        self._cog_names = dict()

        # Emojis
        self.emotes = senko.Emojis()
        self.emotes.load_dir(os.path.join(self.path, "data", "emojis"))

        # Images
        self.images = senko.Images()
        self.images.load_dir(os.path.join(self.path, "data", "images"))

        # Logging
        self.logging = senko.Logging(self)

        # Extensions
        for ext in self.config.extensions:
            self.load_extension(f"cogs.{ext}")

        self.log.info(f"Loaded {len(self.config.extensions)} extension(s).")

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

    @property
    def settings(self):
        """
        Optional[~cogs.settings.SettingsCog]: The settings cog when loaded.
        """
        return self.get_cog("settings")

    # Command methods

    def add_command(self, command):
        """
        Adds a :class:`senko.Command` or :class:`senko.Group` to the
        internal list of commands.

        Extends :meth:`discord.ext.commands.Bot.add_command` with type
        checking and a default cooldown.

        Parameters
        ----------
        command: Union[senko.Command, senko.Group]
            The command to add.

        Raises
        ------
        discord.ext.commands.CommandRegistrationError
            If the command or its alias is already registered by a
            different command.
        TypeError
            If the command passed is not a subclass of :class:`senko.Command`
            or :class:`senko.Group`.
        """
        if not isinstance(command, (senko.Command, senko.Group)):
            raise TypeError(
                f"Command {command!r} does not inherit from senko.Command or senko.Group!"
            )

        super().add_command(command)

        # Add a default cooldown of three seconds / user.
        queue = [command]
        for command in queue:
            if isinstance(command, senko.Group):
                queue += command.commands

            if not command._buckets.valid:
                cooldown = commands.Cooldown(1, 3, commands.BucketType.user)
                command._buckets = commands.CooldownMapping(cooldown)

    # Cog methods

    def _add_locale(self, locale):
        super()._add_locale(locale)

        # Add cog name mappings for locale.
        for cog in list(self.cogs.values()):
            self._add_cog_names(cog, locale)

    def _remove_locale(self, locale):
        super()._remove_locale(locale)

        # Remove cog name mappings for locale.
        self._cog_names.pop(locale.language, None)

    def _add_cog_names(self, cog, locale):
        """
        Add the localization mappings for a cog.

        Parameters
        ----------
        cog: senko.Cog
            The cog for which to add name mappings.
        locale: senko.Locale
            The locale to get the name mappings from.
        """
        try:
            self._cog_names[locale.language]
        except KeyError:
            self._cog_names[locale.language] = self._new_map()

        key = locale(f"{cog.locale_id}_name")
        self._cog_names[locale.language][key] = cog

    def _remove_cog_names(self, cog, locale):
        """
        Remove the localization mappings for a cog.

        Parameters
        ----------
        cog: senko.Cog
            The cog for which to remove the localization mappings.
        locale: senko.Locale
            The locale to remove the name mappings for.
        """
        try:
            mapping = self._cog_names[locale.language]
        except KeyError:
            return

        for key, value in list(mapping.items()):
            if value is cog:
                mapping.pop(key)

    def add_cog(self, cog):
        """
        Adds a cog to the bot.

        Parameters
        ----------
        cog: senko.Cog
            The cog to add to the bot.

        Raises
        ------
        discord.ext.commands.CommandError
            An error occured during loading.
        TypeError
            The cog does not inherit from :class:`senko.Cog`.
        """
        if not isinstance(cog, senko.Cog):
            raise TypeError(f"Cog {cog!r} does not inherit from senko.Cog!")

        super().add_cog(cog)

        # Update cog name cache.
        if self._locale_source is not None:
            for locale in self._locale_source.get_all():
                self._add_cog_names(cog, locale)

    def remove_cog(self, name):
        """
        Remove a cog from the bot.

        Has no effect if no cog with the given name is found.

        Parameters
        ----------
        name: str
            The name of the cog to remove.

        Returns
        -------
        Optional[senko.Cog]
            The cog that was removed.
        """
        cog = self.get_cog(name)
        super().remove_cog(name)

        # Update cog name cache.
        if cog is not None and self._locale_source is not None:
            for locale in self._locale_source.get_all():
                self._remove_cog_names(cog, locale)

        return cog

    def get_cog(self, name, *, locale=None):
        """
        Get a cog by its name.

        If a :class:`senko.Locale` is passed, this method will first
        attempt to resolve the cog by its translated name, and then
        fall back to checking cogs using their original names.

        When the ``case_insensitive`` parameter of the bot is set to
        ``True`` and a ``locale`` is provided the lookup is done case
        insensitively.

        Parameters
        ----------
        name: str
            The name of the cog to get.
        locale: Optional[senko.Locale]
            An optional locale to use to resolve the cog.

        Returns
        -------
        Optional[senko.Cog]
            The requested cog or ``None`` if it was not found.
        """
        if name is None:
            return None

        if locale is not None:
            mapping = self._cog_names.get(locale.language, dict())
            return mapping.get(name, super().get_cog(name))
        else:
            return super().get_cog(name)

    # Context methods

    async def get_context(self, message, cls=senko.CommandContext):
        """
        Get a command context for the given message.

        This method overrides :meth:`discord.ext.commands.Bot.get_context`.

        Parameters
        ----------
        message: discord.Message
            The message to get the context for.
        cls
            The factory class to use to create the command context.
            Defaults to :class:`senko.CommandContext`.

        Returns
        -------
        senko.CommandContext
            The command context for the given message. The type
            of this may change depending on the ``cls`` argument.
        """
        context = await super().get_context(message, cls=cls)

        # Set custom attributes.
        prefix = self.config.prefix
        locale_id = self.config.locale

        if isinstance(message.channel, discord.TextChannel):
            try:
                cog = self.cogs["settings"]
            except KeyError:
                pass
            else:
                settings = await cog.get_guild_settings(message.channel.guild)
                prefix = settings.prefix
                locale_id = settings.locale

        locale = self.locales.get(locale_id)

        context._default_prefix = prefix
        context._locale = locale

        # Ensure that commands are invoked using the locale.
        invoker = context.invoked_with
        context.command = self.get_command(invoker, locale=context.locale)

        return context

    async def get_partial_context(self, user, channel, cls=senko.PartialContext):
        """
        Get a partial context for the given user and channel.

        Parameters
        ----------
        user: Union[discord.User, discord.Member]
            The user to associate with the context.
        channel: discord.TextChannel
            The text channel to associate with the context.
        cls
            The factory class used to create the partial context.
            By default, this is :class:`PartialContext`.

        Returns
        -------
        senko.PartialContext
            A partial context. The type of this may change
            depending on the ``cls`` argument.
        """
        prefix = self.config.prefix
        locale_id = self.config.locale

        if isinstance(channel, discord.TextChannel):
            try:
                cog = self.cogs["settings"]
            except KeyError:
                pass
            else:
                settings = await cog.get_guild_settings(channel.guild)
                prefix = settings.prefix
                locale_id = settings.locale

        locale = self.locales.get(locale_id)

        return cls(self, user, channel, locale, prefix)

    # Runtime methods

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
