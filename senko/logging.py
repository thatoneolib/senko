import datetime
import io
import logging
import traceback

import discord
import senko
import utils
from discord.ext import commands

__all__ = ("Logging",)


class _WebhookHandler(logging.Handler):
    """
    A modifed logging handler that propagates
    emitted records to the logging module.
    """

    def __init__(self, module):
        self._module = module
        super().__init__()

    def emit(self, record):
        if record.name != "senko.logging":
            self._module._send_record(record)


class Logging:
    """
    The internal logging module.

    Logs important events, allows for log records of enabled logging
    domains to be sent through the :data:`config.logging_webhook` and
    allows for exception handlers to be registered for exceptions that
    may be raused during command execution.

    Parameters
    ----------
    bot: senko.Senko
        The bot instance.
    """

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("senko.logging")

        self._webhook = None
        self._logging_handlers = dict()  # str : _WebhookHandler
        self._exception_handlers = dict()  # Type : coroutine

        # Register event handlers.
        self.bot.add_listener(self._on_ready, "on_ready")
        self.bot.add_listener(self._on_shard_ready, "on_shard_ready")
        self.bot.add_listener(self._on_disconnect, "on_disconnect")
        self.bot.add_listener(self._on_resumed, "on_resumed")
        self.bot.add_listener(self._on_command, "on_command")
        self.bot.add_listener(self._on_command_error, "on_command_error")

        # Prepare webhook and add logging handlers.
        if self.bot.config.logging_webhook:
            url = self.bot.config.logging_webhook
            adapter = discord.AsyncWebhookAdapter(self.bot.session)
            self._webhook = discord.Webhook.from_url(url, adapter=adapter)

            # Add logging handlers.
            for domain, level in self.bot.config.logging_domains:
                self.enable_logging(domain, level)
        else:
            self.log.info("Webhook logging disabled (config.logging_webhook is None).")

    async def _on_ready(self):
        self.log.info("Logged in as {0} ({0.id}).".format(self.bot.user))

    async def _on_shard_ready(self, shard_id):
        self.log.info(f"Shard {shard_id} ready.")

    async def _on_disconnect(self):
        self.log.info("Disconnected from Discord!")

    async def _on_resumed(self):
        self.log.info("Session resumed.")

    async def _on_command(self, ctx):
        user = str(ctx.user)
        command = ctx.command.qualified_name
        self.log.debug(f"{user!r} used {command!r}.")

    async def _on_command_error(self, ctx, exc):
        if isinstance(exc, commands.CommandInvokeError):
            exc = exc.__cause__

        handler = self._exception_handlers.get(type(exc))

        if handler is None:
            if isinstance(exc, commands.CommandNotFound):
                return

            ctx.command.reset_cooldown(ctx)
            handler = self._default_handler

        try:
            await handler(ctx, exc)
        except Exception as e:
            t = type(exc).__name__
            self.log.exception(f"An error occured while handling {t!r}!", exc_info=e)

    # Private functions

    async def _default_handler(self, ctx, exc):
        # The default exception handler for command errors.
        #
        # Notifies the user that an unhandled error occured
        # and sends an error log through the logging webhook.
        #
        # This function is used as a fallback when no handler
        # has been registered for an exception.
        command = ctx.command.qualified_name
        self.log.info(f"Handling an unhandled error in {command!r}!", exc_info=exc)

        # Notify user.
        _ = ctx.locale

        # NOTE: Title of the error notification for unhandled errors.
        title = _("{e:critical} Unhandled Error")
        title = self.bot.emotes.format(title)

        # NOTE: Text of the error notification for unhandled errors.
        text = _(
            "**{user}**, an unhandled error has occured. The issue has "
            "been reported to the developer and should be resolved soon. "
            "I am sorry for the inconvenience."
        )
        text = text.format(user=ctx.clean_name)

        try:
            await ctx.embed(title=title, description=text, colour=senko.Colour.red())
        except Exception as e:
            self.log.exception("Could not send unhandled error message!", exc_info=e)

        # Build the error message to send through the webhook.
        if self._webhook is None:
            return

        if ctx.message.edited_at:
            timestamp = ctx.message.edited_at
            footer = f"Edited"
        else:
            timestamp = ctx.message.created_at
            footer = None

        stamp = timestamp.strftime("%d.%m.%Y %H:%M:%S.%f")

        embed = utils.io.build_embed(
            title="Unhandled Command Error",
            description=f"Error report for command `{command}` at `{stamp}`.",
            footer=footer,
            timestamp=timestamp,
            colour=senko.Colour.red(),
        )

        exception = f"{type(exc).__name__}: {exc}"
        exception = utils.string.truncate(exception, 500)

        details = [
            f"• Message: {ctx.message.id} ([link]({ctx.message.jump_url}))",
            f"• Author: {ctx.author} ({ctx.author.id})",
        ]

        if ctx.guild is not None:
            details.append(f"• Guild: {ctx.guild} ({ctx.guild.id})")
            details.append(f"• Channel: #{ctx.channel} ({ctx.channel.id})")
        else:
            details.append(f"• DM Channel: {ctx.channel} ({ctx.channel.id})")

        embed.add_field(name="Details", value="\n".join(details))

        if ctx.message.content:
            display = utils.string.truncate(ctx.message.content, 500)
            embed.add_field(name="Message", value=display, inline=False)

        if ctx.message.attachments:
            attachments = "\n".join([a.url for a in ctx.message.attachments])
            embed.add_field(name="Attachments", value=attachments, inline=False)

        trace = traceback.format_exception(None, exc, exc.__traceback__)
        complete = "".join(trace)

        display = utils.string.truncate(complete, 1000)
        embed.add_field(name="Traceback", value=f"```\n{display}```", inline=False)

        sep = "-" * 112
        content = (
            f'Error report for command "{ctx.command.qualified_name}" '
            f"at {stamp}.\n{sep}\n{ctx.message.content}\n{sep}\n{complete}"
        )
        buffer = io.BytesIO(content.encode("utf-8"))
        file = discord.File(buffer, f"traceback.txt")

        kwargs = dict()
        if self.bot.user is not None:
            kwargs["username"] = self.bot.user.name
            kwargs["avatar_url"] = self.bot.user.avatar_url

        try:
            await self._webhook.send(embed=embed, file=file, **kwargs)
        except Exception as exc:
            self.log.exception(
                "Failed to send error log through webhook!", exc_info=exc
            )

    def _send_record(self, record):
        # Sends an embed for a log record through the logging webhook.
        if self._webhook is None:
            return

        timestamp = datetime.datetime.fromtimestamp(record.created)

        colours = {
            logging.DEBUG: senko.Colour.purple(),
            logging.INFO: senko.Colour.light_blue(),
            logging.WARNING: senko.Colour.yellow(),
            logging.ERROR: senko.Colour.red(),
            logging.CRITICAL: senko.Colour.dark_red(),
        }

        embed = discord.Embed(
            title=record.levelname.title(),
            description=record.msg % record.args,
            colour=colours.get(record.levelno, senko.Colour.red()),
            timestamp=timestamp,
        )

        embed.set_footer(text=f"Logged by {record.name!r}")
        kwargs = dict()

        # For warnings and higher, include the location.
        if record.levelno >= logging.WARNING:
            embed.add_field(
                name="Location",
                value=f"File {record.pathname!r}, line {record.lineno}, in {record.funcName!r}.",
            )

        # For errors and higher, include exception info, if set.
        if record.levelno >= logging.ERROR and record.exc_info is not None:
            full_trace = "".join(traceback.format_exception(*record.exc_info))

            if len(full_trace) > 1000:
                shown_trace = f"```\n{full_trace[:990]}...```"
                buffer = io.BytesIO(full_trace.encode("utf-8"))
                attachment = discord.File(buffer, f"traceback.txt")
                kwargs["file"] = attachment
            else:
                shown_trace = f"```\n{full_trace}...```"

            embed.add_field(name="Traceback", value=shown_trace, inline=False)

        if self.bot.user is not None:
            kwargs["username"] = self.bot.user.name
            kwargs["avatar_url"] = self.bot.user.avatar_url

        self.bot.loop.create_task(self._webhook.send(embed=embed, **kwargs))

    # Public functions

    def shutdown(self):
        """
        Unregister all event listeners and remove all logging handlers.
        """
        # Disable exception handlers.
        self._exception_handlers = dict()

        # Remove logging handlers
        domains = list(self._logging_handlers.keys())
        for domain in domains:
            self.disable_logging(domain)

        # Remove event listeners
        self.bot.remove_listener(self._on_ready, "on_ready")
        self.bot.remove_listener(self._on_shard_ready, "on_shard_ready")
        self.bot.remove_listener(self._on_disconnect, "on_disconnect")
        self.bot.remove_listener(self._on_resumed, "on_resumed")
        self.bot.remove_listener(self._on_command, "on_command")
        self.bot.remove_listener(self._on_command_error, "on_command_error")

    def enable_logging(self, domain, level=logging.WARNING):
        """
        Enable webhook logging for a logging domain.

        Parameters
        ----------
        domain: str
            The name of the domain for which to enable webhook logging.
        level: Optional[int]
            The log level at which to send records through the webhook.
        """
        # Update level for existing handler.
        if domain in self._logging_handlers:
            self._logging_handlers[domain].setLevel(level)
            return

        handler = _WebhookHandler(self)
        handler.setLevel(level)
        logging.getLogger(domain).addHandler(handler)
        self._logging_handlers[domain] = handler

    def disable_logging(self, domain):
        """
        Disable webhook logging for a logging domain.

        Parameters
        ----------
        domain: str
            The name of the domain for which to disable webhook logging.
        """
        handler = self._logging_handlers.pop(domain, None)
        logging.getLogger(domain).removeHandler(handler)

    def add_handler(self, exception, handler):
        """
        Add a handler for an exception.

        Overrides any previously registered handlers
        for the given exception type.

        Parameters
        ----------
        exception: type
            The exception type for which to add the handler.
        handler: callable
            The function to be called when :func:`discord.on_command_error`
            is dispatched for the given ``exception``. Must be a coroutine
            that takes a :class:`senko.CommandContext` as its first, and
            an exception as its second parameter.
        """
        if not issubclass(exception, Exception):
            raise TypeError("exception must be derived from Exception!")

        if not callable(handler):
            raise TypeError("handler must be a callable!")

        self._exception_handlers[exception] = handler

    def remove_handler(self, exception):
        """
        Remove the handler for an exception.

        Parameters
        ----------
        exception: type
            The exception type for which to remove the handler.
        """
        self._exception_handlers.pop(exception, None)

    def get_handler(self, exception):
        """
        Get the handler for an exception.

        Parameters
        ----------
        exception: type
            The exception type for which to get the handler.

        Returns
        -------
        Optional[callable]
            A coroutine function that has been registered as
            the handler for the given exception type, or ``None``
            if no handler has been registered.
        """
        return self._exception_handlers.get(exception)
