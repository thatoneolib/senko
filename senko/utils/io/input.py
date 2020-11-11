import asyncio
import inspect
import typing

import senko
from discord.ext import commands

__all__ = (
    "input",
    "Input",
    "InputError",
    "InputTimeoutError",
    "InputStateError",
    "InputConversionError",
    "InputUnionConversionError",
)


class InputError(Exception):
    """
    Base exception for :class:`~senko.utils.io.Input`-related errors.
    """


class InputTimeoutError(InputError):
    """
    Exception raised when an :class:`~senko.utils.io.Input` times out.

    Inherits from :exc:`~.InputError`.
    """


class InputStateError(InputError):
    """
    Exception raised when attempting to perform an operation on
    an :class:`~senko.utils.io.Input` that conflicts with its state.

    Inherits from :exc:`~.InputError`.
    """


class InputConversionError(InputError):
    """
    Exception raised when a user input conversion fails.

    Inherits from :exc:`~.InputError`.

    Parameters
    ----------
    converter: discord.ext.commands.Converter
        The converter that failed.
    original: Exception
        The original exception that was raised.
    """

    def __init__(self, converter, original):
        self.converter = converter
        self.original = original


class InputUnionConversionError(InputError):
    """
    Exception raised when a user input conversion for a :py:class:`typing.Union`
    converter fails.

    Parameters
    ----------
    converter: discord.ext.commands.Converter
        The converter that failed.
    errors: List[Exception]
        A list of exceptions that were raised by the unified converters.
    """

    def __init__(self, converter, errors):
        self.converter = converter
        self.errors = errors


class Input:
    r"""
    Helper class for input prompts.

    Uses a :class:`discord.ext.commands.Converter` to transform user input
    into the desired type. Returns the converted value upon parsing a valid
    input. During an ongoing conversion, no further conversions can be ran.

    Parameters
    ----------
    ctx: Union[senko.CommandContext, senko.PartialContext]
        The context under which to run the prompt.
    converter: Optional[discord.ext.commands.Converter]
        The converter to use to convert the user input. Attempts to resolve
        converters that do not inherit from :class:`discord.ext.commands.Converter`
        to the converters defined in ``senko.converters``. Defaults to ``str``.
    timeout: Optional[float]
        Delay in seconds after which the prompt should time out. Defaults to 60.
    raise_errors: Optional[bool]
        Whether to raise conversion errors. Defaults to ``False``.
    raise_timeout: Optional[bool]
        Whether to raise when timing out. Defaults to ``False``.
    delete_after: Optional[bool]
        Whether to delete the prompt and user input upon completing.
        Defaults to ``False``.
    \*\*kwargs
        Keyword arguments to pass into :func:`senko.utils.io.build_embed` to
        build the input prompt embed from.
    """

    def __init__(
        self,
        ctx,
        converter=None,
        timeout=60.0,
        raise_errors=False,
        raise_timeout=False,
        delete_after=False,
        **kwargs,
    ):
        self.ctx = ctx
        self.bot = ctx.bot
        self.loop = ctx.loop
        self.user = ctx.user
        self.channel = ctx.channel

        self.converter = converter
        if self.converter is None:
            self.converter = str

        self.timeout = timeout
        self.raise_errors = raise_errors
        self.raise_timeout = raise_timeout
        self.delete_after = delete_after
        self.kwargs = kwargs

        # Runtime variables
        self._started = False
        self._result = self.loop.create_future()
        self._converting = asyncio.Lock()
        self._message = None
        self._user_message = None

    async def _convert(self, converter, argument):
        """
        Attempt to convert the argument.

        This mimics discord.ext.commands.Command._actual_conversion.
        """
        # Resolve primitive types.
        if converter is bool:
            converter = senko.converters.Bool
        elif converter is int:
            converter = senko.converters.Int
        elif converter is float:
            converter = senko.converters.Float
        elif converter is str:
            pass

        try:
            module = converter.__module__
            if module.startswith("discord.") and not module.endswith("converter"):
                converter_name = converter.__name__
                converter = getattr(senko.converters, converter_name, converter)
        except AttributeError:
            pass

        # Do the conversion step. We do not wrap this in try-catch as we
        # handle exceptions in _on_message already and raise our own exception
        # anyway.

        # Check for an uninitialized converter.
        if inspect.isclass(converter):
            if issubclass(converter, commands.Converter):
                instance = converter()
                return await instance.convert(self.ctx, argument)
            else:
                method = getattr(converter, "convert", None)
                if method is not None and inspect.ismethod(method):
                    return await method(self.ctx, argument)

        # Call the convert method for initialized converters.
        elif isinstance(converter, commands.Converter):
            return await converter.convert(self.ctx, argument)

        # Otherwise just call the converter directly.
        return converter(argument)

    async def _on_message(self, message):
        """
        Handle :func:`discord.on_message` events and parse user input.

        Attempts to convert the content of messages sent by the input
        owner in the input channel.

        On a successful parse, sets the internal result to the converted value.

        When an error is encountered while parsing, and ``raise_errors`` is
        enabled, the internal result is set to the corresponding exception.

        For :py:class:`typing.Union` converters, the raised exception is a
        :exc:`~.InputUnionConversionError`.

        This mimics discord.ext.commands.Command.do_conversion.
        """
        if message.author != self.user or message.channel != self.channel:
            return

        if self._converting.locked():
            return

        async with self._converting:
            try:
                origin = self.converter.__origin__
            except AttributeError:
                pass
            else:
                if origin is typing.Union:
                    errors = []
                    for converter in self.converter.__args__:
                        try:
                            result = await self._convert(converter, message.content)
                        except Exception as e:
                            errors.append(e)
                        else:
                            self._user_message = message
                            self._result.set_result(result)
                            return

                # If all conversion attempts failed, raise.
                if self.raise_errors:
                    error = InputUnionConversionError(self.converter, errors)
                    self._result.set_exception(error)
                return

            # Otherwise simply call _convert.
            try:
                result = await self._convert(self.converter, message.content)
            except Exception as e:
                if self.raise_errors:
                    error = InputConversionError(self.converter, e)
                    self._result.set_exception(error)
                return
            else:
                self._user_message = message
                self._result.set_result(result)

    async def _send_message(self):
        """
        Sends the message for the prompt.
        """
        return await self.ctx.embed(**self.kwargs)

    async def run(self):
        """
        Run the prompt.

        Raises
        ------
        InputStateError
            Exception raised when the prompt was already started.
        InputTimeoutError
            Exception raised when the prompt times out.
        InputConversionError
            Exception raised when the conversion fails.
        InputUnionConversionError
            Exception raised when the conversion fails.

        Returns
        -------
        Any
            The converted user input or ``None`` if the
            prompt timed out.
        """
        if self._result.done():
            raise InputStateError("Input already finished.")
        elif self._started:
            raise InputStateError("Input already stated.")

        # Mark as started and send initial message.
        self._started = True
        self._message = await self._send_message()

        # Start listening to events.
        self.bot.add_listener(self._on_message, "on_message")

        # Wait for valid input or timeout.
        try:
            await asyncio.wait_for(self._result, timeout=self.timeout)
        except asyncio.TimeoutError:
            # Recreate the future as it is cancelled on timeout.
            self._result = self.loop.create_future()
            if self.raise_timeout:
                self._result.set_exception(InputTimeoutError("Input timed out."))
            else:
                self._result.set_result(None)
        except:
            # If we did not time out, it is most likely that raise_errors
            # is enabled and we caught a conversion error.
            pass

        # Stop listening.
        self.bot.remove_listener(self._on_message, "on_message")

        # Delete messages.
        if self.delete_after:
            remove = [self._message]
            if self.channel.permissions_for(self.ctx.me).manage_messages:
                remove.append(self._user_message)

            for message in remove:
                try:
                    await message.delete()
                except:
                    pass

        elif len(self._message.embeds) > 0:
            embed = self._message.embeds[0]
            embed.colour = senko.Colour.disabled()
            try:
                await self._message.edit(embed=embed)
            except:
                pass

        # Return result or raise exception.
        return self._result.result()


async def input(ctx, *args, **kwargs):
    r"""
    Create and run an :class:`~senko.utils.io.Input` and return its result.

    Parameters
    ----------
    ctx: Union[senko.CommandContext, senko.PartialContext]
        The context under which to run the prompt.
    \*args
        Positional arguments to pass into :class:`~senko.utils.io.Input`.
    \*\*kwargs
        Keyword arguments to pass into :class:`~senko.utils.io.Input`.

    Raises
    ------
    InputTimeoutError
        Exception raised when the prompt times out.
    InputConversionError
        Exception raised when the conversion fails.
    InputUnionConversionError
        Exception raised when the conversion fails.

    Returns
    -------
    Any
        The converted user input or ``None`` if the
        prompt timed out.
    """
    prompt = Input(ctx, *args, **kwargs)
    return await prompt.run()
