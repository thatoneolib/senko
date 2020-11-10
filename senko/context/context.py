from datetime import datetime, timezone

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

    async def embed(self, content=None, **kwargs):
        r"""
        Send an embed in the context channel.

        This function automatically sets the :attr:`discord.Embed.footer`
        of the embed to the avatar and name of the user associated with
        the context.

        The :attr:`discord.Embed.timestamp` is set to the current time.

        Parameters
        ----------
        content: Optional[str]
            The message content.
        tts: Optional[bool]
            Indicates if the message should be sent using tts.
        file: Optional[discord.File]
            A file to upload
        files: List[discord.File]
            A list of files to upload. Must not exceed 10.
        nonce: int
            The nonce to use for sending this message. If the message
            was sent successfully, it wil have a nonce with this value.
        delete_after: Optional[float]
            The number of seconds to wait before deleting the message
            that was sent. If deletion fails, it is silently ignored.
        allowed_mentions: Optional[discord.AllowedMentions]
            Controls the mentions being processed in this message.
        \*\*kwargs
            Keyword arguments to pass into :meth:`senko.utils.io.build_embed`.

        Returns
        -------
        discord.Message
            The message that was sent.
        """
        # Extract regular parameters.
        content = content
        tts = kwargs.pop("tts", False)
        file = kwargs.pop("file", None)
        files = kwargs.pop("files", None)
        delete_after = kwargs.pop("delete_after", None)
        nonce = kwargs.pop("nonce", None)
        allowed_mentions = kwargs.pop("allowed_mentions", None)

        # Apply timestamp and user information.
        footer_dict = kwargs.pop("footer", dict())
        footer_text = None
        footer_icon = self.user.avatar_url

        _ = self.locale
        # Note: Format string for embed footers with user indicator.
        # DEFAULT: {name} • {footer}
        fmt = _("{name} • {footer}")

        if isinstance(footer_dict, str):
            footer_text = fmt.format(name=self.user, footer=footer_dict)
        elif "text" in footer_dict:
            footer_text = fmt.format(name=self.user, footer=footer_dict.get("text"))
        else:
            footer_text = str(self.user)

        kwargs["footer"] = dict(text=footer_text, icon_url=footer_icon)
        kwargs["timestamp"] = datetime.now(tz=timezone.utc)

        embed = senko.utils.io.build_embed(**kwargs)

        # Send and return the message.
        return await self.send(
            content=content,
            tts=tts,
            file=file,
            files=files,
            embed=embed,
            delete_after=delete_after,
            nonce=nonce,
            allowed_mentions=allowed_mentions,
        )

    async def input(self, *args, **kwargs):
        r"""
        Create an :class:`~senko.utils.io.Input` and return its result.

        Passes this context as the ``ctx`` parameter.

        Parameters
        ----------
        \*args
            Positional arguments to pass into :class:`~senko.utils.io.Input`.
        \*\*kwargs
            Keyword arguments to pass into :class:`~senko.utils.io.Input`.

        Raises
        ------
        ~senko.utils.io.InputTimeoutError
            Exception raised when the prompt times out.
        ~senko.utils.io.InputConversionError
            Exception raised when the conversion fails.
        ~senko.utils.io.InputUnionConversionError
            Exception raised when the conversion fails.

        Returns
        -------
        Any
            The converted user input or ``None`` if the input timed out.
        """
        prompt = senko.utils.io.Input(self, *args, **kwargs)
        return await prompt.run()
