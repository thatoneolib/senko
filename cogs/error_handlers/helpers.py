import time

__all__ = (
    "usage_for_command",
    "help_invocation_for_command",
    "hint_for_command",
    "count_calls",
)

# Localization helpers

def usage_for_command(prefix, command, locale):
    """
    Get the command usage string for a command.

    Parameters
    ----------
    prefix: str
        The command prefix to show.
    command: senko.Command
        The command to get the usage string for.
    locale: senko.Locale
        The locale to get the usage string for.

    Returns
    -------
    str
        The usage string for the given command in the
        given locale.
    """
    command_name = command.get_qualified_name(locale)
    signature = command.get_signature(locale)
    return f"{prefix}{command_name} {signature}"

def help_invocation_for_command(prefix, command, locale):
    """
    Get the help command invocation for a command.

    Parameters
    ----------
    prefix: str
        The command prefix to show.
    command: senko.Command
        The command to get the help invocation for.
    locale: senko.Locale
        The locale to get the help invocation for.

    Returns
    -------
    str
        The help invocation for the given command in the
        given locale.
    """
    command_name = command.get_qualified_name(locale)
    help_name = _("#command_help_name")
    return f"{prefix}{help_name} {command_name}"

def hint_for_command(prefix, command, locale):
    """
    Get the command usage field for a command.

    Displays the usage string of the command and how to
    view its page through the help command.

    Parameters
    ----------
    prefix: str
        The prefix to show.
    command: senko.Command
        The command to generate the usage field for.
    locale: senko.Locale
        The locale to get the field in.

    Returns
    -------
    dict
        A dictionary containing the ``name`` and ``value``
        keys to be added to an embed as a field.
    """
    _ = locale

    # NOTE: Title of the hint field in the error message for missing required arguments.
    hint_name = _("Hints")

    # NOTE: Text of the hint field in the error message for missing required arguments.
    hint_text = _("Usage: `{usage}`\nUse `{help}` for more information.")

    usage = usage_for_command(prefix, command, locale)
    help = help_invocation_for_command(prefix, command, locale)

    return dict(name=hint_name, value=hint_text.format(usage=usage, help=help))

# Call counting decorator

class count_calls(object):
    """
    A decorator class that counts the decorated function's invocations.

    Passes a keyword parameter named after ``keyword`` into the decorated
    method. The value of the parameter is equal to the amount of times the
    function has been called within the ``timeout``.

    The decorated function must take a :class:`senko.CommandContext` as its
    first parameter.

    Parameters
    ----------
    timeout: float
        The timeout in seconds after which to reset the call count back to 0.
    bucket: :class:`discord.ext.commands.BucketType`
        The cooldown bucket type to use.
    keyword: Optional[str]
        The name of the keyword argument to pass into the decorated function.
        Must be a valid Python identifier. Defaults to ``calls``.
    """

    __slots__ = ("timeout", "bucket", "keyword", "_cache")

    def __init__(self, timeout, bucket, keyword=None):
        self.timeout = timeout
        self.bucket = bucket
        self.keyword = keyword

        if self.keyword is None:
            self.keyword = "calls"

        if not self.keyword.isidentifier():
            raise ValueError("keyword must be a valid python identifier!")

        self._cache = dict()

    def _get_key(self, ctx):
        """
        Get a unique key for the bucket type and given context.

        Parameters
        ----------
        ctx: senko.CommandContext
            The invocation context.

        Returns
        -------
        Tuple[...]
            A tuple to use as the key.
        """
        # Get a key for the internal bucket type and invoked command.
        base = self.bucket.get_key(ctx.message)
        if not isinstance(base, tuple):
            base = (base,)

        # Get the qualified command name.
        command = None
        if ctx.command is not None:
            command = ctx.command.qualified_name

        return (command,) + base

    def _get_calls(self, key):
        """
        Get the total amount of calls made for the given key.

        Increments the amount of calls made for the given key by 1.

        Parameters
        ----------
        key: Tuple[...]
            A key as returned by ``_get_key``.

        Returns
        -------
        int
            The amount of calls made for the key within the time frame.
        """
        # Remove expired cooldowns.
        now = time.time()
        expired = [k for k, v in self._cache.items() if (now - v[1] > self.timeout)]

        for k in expired:
            del self._cache[k]

        # Get made calls and timestamp. Increment calls by 1.
        # Get the number of attempts since the function
        # went on cooldown for the provided key.
        calls, timestamp = self._cache.get(key, (0, now))
        self._cache[key] = (calls + 1, timestamp)
        return calls

    def __call__(self, func):
        # Returns a decorator that injects the calls keyword.
        async def predicate(ctx, *args, **kwargs):
            key = self._get_key(ctx)
            calls = self._get_calls(key)
            kwargs[self.keyword] = calls
            await func(ctx, *args, **kwargs)

        # Copy the docstring so sphinx knows what's up.
        predicate.__doc__ = func.__doc__
        return predicate
