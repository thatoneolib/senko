from .input import Input, InputError

__all__ = ("ChoiceCancelledError", "Choice", "choice")


class ChoiceCancelledError(InputError):
    """
    Exception raised when a :class:`~senko.utils.io.Choice`
    is cancelled.

    Inherits from :exc:`~senko.utils.io.InputError`.
    """


class Choice(Input):
    r"""
    An :class:`~senko.utils.io.Input` that prompts the user to choose
    from a set of options.

    Parameters
    ----------
    ctx: Union[senko.CommandContext, senko.PartialContext]
        The context under which to run the prompt.
    options: Union[List[Tuple[str, Any]], Dict[str, Any]]
        A dictionary or list of options for the context owner to choose from.
    allow_cancel: Optional[bool]
        Whether to add an additional option to cancel the prompt.
        Defaults to ``False``.
    timeout: Optional[float]
        Delay in seconds after which the prompt should time out.
        Defaults to 60.
    raise_timeout: Optional[bool]
        Whether to raise :exc:`~.InputTimeoutError` when timing out.
        Defaults to ``False``.
    raise_errors: Optional[bool]
        Whether to raise conversion errors.
        Defaults to ``False``.
    raise_cancel: Optional[bool]
        Whether to raise :exc:`~.ChoiceCancelledError` when the prompt
        is cancelled. Defaults to ``False``.
    delete_after: Optional[bool]
        Whether to delete the prompt and user input upon completing.
        Defaults to ``False``.
    \*\*kwargs
        Keyword arguments to pass into :func:`senko.utils.io.build_embed`
        to build the choice prompt embed from.

    Raises
    ------
    ValueError
        When ``options`` contains 0 or more than 10 options, or when
        ``None`` is used as a value when ``allow_cancel`` is enabled.
    """

    def __init__(
        self,
        ctx,
        options,
        allow_cancel=False,
        timeout=60.0,
        raise_timeout=False,
        raise_errors=False,
        raise_cancel=False,
        delete_after=False,
        **kwargs,
    ):
        # Initialize superclass.
        super().__init__(
            ctx,
            converter=self._do_conversion,
            timeout=timeout,
            raise_timeout=raise_timeout,
            raise_errors=raise_errors,
            delete_after=delete_after,
            **kwargs,
        )

        # Generate options mapping.
        if isinstance(options, dict):
            options = options.items()

        # Maps input strings to (text, value) pairs.
        self.options = dict((str(p[0]), p[1]) for p in enumerate(options, 1))

        # Maps input strings to values. Used for value resolution.
        self.inputs = {key: pair[1] for key, pair in self.options.items()}

        # Add cancel button
        self.allow_cancel = allow_cancel
        self.raise_cancel = raise_cancel

        if not self.allow_cancel:
            return

        for pair in self.options.values():
            if pair[1] is None:
                raise ValueError(
                    "Option values must not be None when allow_cancel is enabled!"
                )

        _ = ctx.locale

        # NOTE: Input for the option to cancel a choice prompt.
        cancel_input = _("cancel")
        self.inputs[cancel_input.casefold()] = None

    def _do_conversion(self, string):
        """
        Attempt to resolve the input string to an option.
        """
        value = self.inputs[string.casefold()]

        if value is None and self.raise_cancel:
            raise ChoiceCancelledError()

        return value

    async def _send_message(self):
        _ = self.ctx.locale

        # NOTE: Name of the "Options" field in choice prompts.
        field_name = _("Options")

        # NOTE: Format for listed options in choice prompts.
        # NOTE: Option is replaced with a number, description with
        # NOTE: the option text.
        line_fmt = _("`{option}` {description}")

        # NOTE: Text for the option to cancel a choice prompt.
        cancel_text = _("Enter **{}** to cancel the selection.")

        # NOTE: User input to cancel a choice prompt.
        cancel_input = _("cancel")
        cancel_text = cancel_text.format(cancel_input)

        # Generate the options field.
        lines = []
        for key, pair in self.options.items():
            lines.append(line_fmt.format(option=key, description=pair[0]))

        if self.allow_cancel:
            lines.append("")
            lines.append(cancel_text)

        field_value = "\n".join(lines)

        # Build keyword arguments.
        kwargs = self.kwargs.copy()
        fields = self.kwargs.get("fields", []).copy()
        fields.append(dict(name=field_name, value=field_value, inline=False))
        kwargs["fields"] = fields

        return await self.ctx.embed(**kwargs)


async def choice(ctx, options, **kwargs):
    r"""
    Shortcut function to create a :class:`~senko.utils.io.Choice`.

    Takes the same parameters as :class:`~senko.utils.io.Choice`.

    Parameters
    ----------
    ctx: Union[senko.CommandContext, senko.PartialContext]
        The context under which to run the prompt.
    \*args
        Positional arguments to pass into :class:`~senko.utils.io.Choice`.
    \*\*kwargs
        Keyword arguments to pass into :class:`~senko.utils.io.Choice`.

    Raises
    ------
    InputTimeoutError
        Exception raised when the prompt times out and ``raise_timeout`` is enabled.
    InputConversionError
        Exception raised when the conversion fails and ``raise_errors`` is enabled.
    InputUnionConversionError
        Exception raised when the conversion fails and ``raise_errors`` is enabled.
    ChoiceCancelledError
        Exception raised when the choice is cancelled.

    Returns
    -------
    Any
        The return value of the prompt.
    """
    prompt = Choice(ctx, options, **kwargs)
    return await prompt.run()
