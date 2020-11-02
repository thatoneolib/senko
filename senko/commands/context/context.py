import babel
import discord
import senko
from discord.ext import commands


class CommandContext(commands.Context):
    """
    A modified :class:`discord.ext.commands.Context` implementation.

    This class contains additional properties and methods that simplify
    some common use cases for context objects.

    The following attributes are not set when the class is intialized
    and are instead manually set in :meth:`senko.Senko.get_context`:

    * :attr:`senko.CommandContext.locale`
    * :attr:`senko.CommandContext.default_Prefix`
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set new attributes.
        bot = kwargs.get("bot")
        self._locale = senko.NullLocale(bot.config.locale)
        self._default_prefix = bot.config.prefix

        # Set new variables.
        self._connection = None

    @property
    def loop(self):
        """
        asyncio.AbstractEventLoop: The event loop used by the bot.
        """
        return self.bot.loop

    @property
    def session(self):
        """
        aiohttp.ClientSession: The client session of the bot.
        """
        return self.bot.session

    @property
    def db(self):
        """
        asyncpg.pool.Pool: The database connection pool of the bot.
        """
        return self.bot.db

    @discord.utils.cached_property
    def user(self):
        """
        Union[discord.User, discord.Member]: Alias for
        :attr:`~senko.Context.author`.
        """
        return self.author

    @property
    def clean_name(self):
        """
        str: The cleaned display name of the context author.

        Equivalent to the following calls:

        .. code-block:: python3

            name = ctx.author.display_name
            name = discord.utils.escape_markdown(name)
        """
        return discord.utils.escape_markdown(self.author.display_name)

    @property
    def display_name(self):
        """
        str: The display name of the context author.

        Equivalent to calling :attr:`senko.Context.author.display_name`.
        """
        return self.author.display_name

    @property
    def default_prefix(self):
        """
        str: The default command prefix for the context. This is either the
        guild prefix, if applicable, or :data:`config.prefix`.
        """
        return self._default_prefix

    @property
    def locale(self):
        """
        Union[senko.Locale, senko.NullLocale]: The locale to use for this
        context. Defaults to a Defaults to a :class:`senko.NullLocale` with
        ``language`` set to :data:`config.locale`.
        """
        return self._locale

    @discord.utils.cached_property
    def babel_locale(self):
        """
        babel.core.Locale: The babel locale for the locale of this context.
        Returns the locale for the default locale if the locale is not
        supported. If that locale is not supported either, returns the locale
        for ``en_GB``.
        """
        try:
            return babel.Locale.parse(self.locale.language)
        except babel.UnknownLocaleError:
            try:
                return babel.Locale.parse(self.bot.config.locale)
            except babel.UnknownLocaleError:
                return babel.Locale.parse("en_GB")
