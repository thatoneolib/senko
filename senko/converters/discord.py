import inspect

from babel.core import UnknownLocaleError
from babel.numbers import NumberFormatError, parse_decimal, parse_number
from senko import Colour as SenkoColour

from discord.ext import commands

from .utils import clean

__all__ = (
    "Member",
    "User",
    "Message",
    "TextChannel",
    "VoiceChannel",
    "CategoryChannel",
    "Invite",
    "Role",
    "Colour",
    "Emoji",
    "PartialEmoji",
)


class Member(commands.MemberConverter):
    """
    Converts to :class:`discord.Member`.

    Inherits from :class:`discord.ext.commands.MemberConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.MemberNotFound as e:
            _ = ctx.locale
            # NOTE: Error message for the member converter.
            message = _('I could not find someone named "{}" on this server.')
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e


class User(commands.UserConverter):
    """
    Converts to :class:`discord.User`.

    Inherits from :class:`discord.ext.commands.UserConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.UserNotFound as e:
            _ = ctx.locale
            # NOTE: Error message for the user converter.
            message = _('I could not find a user named "{}".')
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e


class Message(commands.MessageConverter):
    """
    Converts to a :class:`discord.Message`.

    Inherits from :class:`discord.ext.commands.MessageConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.MessageNotFound as e:
            _ = ctx.locale
            # NOTE: Error message for the message converter.
            message = _("I could not find the message.")
            raise commands.BadArgument(message) from e
        except commands.ChannelNotFound as e:
            _ = ctx.locale
            # NOTE: Error message for the message converter.
            message = _("I could not find the channel for the message.")
            raise commands.BadArgument(message) from e
        except commands.ChannelNotReadable as e:
            _ = ctx.locale
            # NOTE: Error message for the message converter.
            message = _("I could not read the channel for the message.")
            raise commands.BadArgument(message) from e


class TextChannel(commands.TextChannelConverter):
    """
    Converts to a :class:`discord.TextChannel`.

    Inherits from :class:`discord.ext.commands.TextChannelConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.ChannelNotReadable as e:
            _ = ctx.locale
            # NOTE: Error message for the text channel converter.
            message = _('I could not find the text channel "{}".')
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e


class VoiceChannel(commands.VoiceChannelConverter):
    """
    Converts to a :class:`discord.VoiceChannel`.

    Inherits from :class:`discord.ext.commands.VoiceChannelConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.ChannelNotFound as e:
            _ = ctx.locale
            # NOTE: Error message for the voice channel converter.
            message = _('I could not find the voice channel "{}".')
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e


class CategoryChannel(commands.CategoryChannelConverter):
    """
    Converts to a :class:`discord.CategoryChannel`.

    Inherits from :class:`discord.ext.commands.CategoryChannel`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.BadArgument as e:
            _ = ctx.locale
            # NOTE: Error message for the channel category converter.
            message = _('The channel category "{}" could not be found.')
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e


class Invite(commands.InviteConverter):
    """
    Converts to :class:`discord.Invite`.

    Inherits from :class:`discord.ext.commands.InviteConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.BadInviteArgument as e:
            _ = ctx.locale
            # NOTE: Error message for the invite converter.
            message = _("The invite `{}` is invalid or expired.")
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e


class Role(commands.RoleConverter):
    """
    Converts to :class:`discord.Role`.

    Inherits from :class:`discord.ext.commands.RoleConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.RoleNotFound as e:
            _ = ctx.locale
            # NOTE: Error message for the role converter.
            message = _('The role "{}" could not be found.')
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e


class Colour(commands.ColourConverter):
    """
    Converts to a :class:`senko.Colour`.

    Inherits from :class:`discord.ext.commands.ColourConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.BadColourArgument as e:

            # Attempt to use the overrides from our custom colour class.
            method = getattr(SenkoColour, argument.replace(" ", "_"), None)
            if method is not None and inspect.ismethod(method):
                return method()

            _ = ctx.locale
            # NOTE: Error message for the colour converter.
            message = _(
                "I could not interpret `{}` as a valid colour. Please try a hex "
                "code or the integer value of the colour."
            )
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e


class Emoji(commands.EmojiConverter):
    """
    Converts to :class:`discord.Emoji`.

    Inherits from :class:`discord.ext.commands.EmojiConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.EmojiNotFound as e:
            _ = ctx.locale
            # NOTE: Error message for the emoji converter.
            message = _('I could not find the "{}" emoji.')
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e


class PartialEmoji(commands.PartialEmojiConverter):
    """
    Converts to :class:`discord.PartialEmoji`.

    Inherits from :class:`discord.ext.commands.PartialEmojiConverter`.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.PartialEmojiConversionFailure as e:
            _ = ctx.locale
            # NOTE: Error message for the emoji converter.
            message = _('I could not find the "{}" emoji.')
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned)) from e
