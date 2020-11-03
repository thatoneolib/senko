import discord
import senko

from .context import CommandContext


class PartialContext(CommandContext):
    """
    A custom :class:`~senko.Context` implementation.

    Instead of representing a command invocation context, this context
    implementation is used to represent a conversation context between
    the bot and a user.

    Due to not being based on a :class:`discord.Message` object, some of
    the properties of the original context may be ``None`` for instances
    of this context.

    Parameters
    ----------
    bot: senko.Senko
        The bot instance.
    user: Union[discord.User, discord.Member]
        The user for this context.
    channel: Union[discord.TextChannel, discord.DMChannel]
        The text channel for this context.
    locale: senko.Locale
        The locale to use for this context.
    prefix: str
        The default prefix for the context. When created for a
        text channel in a guild, this is the prefix for the guild.
        Otherwise this is the default prefix.
    """

    def __init__(self, bot, user, channel, locale, prefix):
        self.bot = bot
        self._user = user
        self._channel = channel

        # As we can not call the parent constructor we initialize
        # the default arguments ourself.
        self.message = None
        self.args = []
        self.kwargs = {}
        self.prefix = prefix  # As we have no other prefix available.
        self.command = None
        self.view = None
        self.invoked_with = None
        self.invoked_subcommand = None
        self.subcommand_passed = None
        self.command_failed = False

        # Normally this is acquired through Message._state, but we can
        # get a reference to the same object through Bot._connection.
        self._state = self.bot._connection

        # Set new attributes.
        self._locale = locale
        self._default_prefix = prefix
        self._connection = None

    async def _get_channel(self):
        # Helper method required by discord.abc.Messageable
        return self.channel

    @property
    def author(self):
        """
        Union[discord.User, discord.Member]: Returns the user associated with
        the context.
        """
        return self._user

    @discord.utils.cached_property
    def guild(self):
        """
        Optional[discord.Guild]: The guild associated with this context.
        """
        return getattr(self._channel, "guild", None)

    @property
    def channel(self):
        """
        discord.TextChannel: The text channel associated with this context.
        """
        return self._channel
