from .choice import Input

__all__ = ("YesNo", "yesno")

class YesNo(Input):
    r"""
    A :class:`~senko.utils.io.Input` for boolean values.

    Prompts the user to choose yes or no, and returns the
    appropriate boolean value.

    Parameters
    ----------
    ctx: Union[senko.CommandContext, senko.PartialContext]
        The context under which to run the prompt.
    timeout: Optional[float]
        Delay in seconds after which the prompt should time out. Defaults to 60.
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
        timeout=60,
        raise_timeout=False,
        delete_after=False,
        **kwargs,
    ):
        # Initialize superclass
        super().__init__(
            ctx,
            converter=bool,
            ignore_errors=True,
            timeout=timeout,
            raise_timeout=raise_timeout,
            raise_errors=False,
            delete_after=delete_after,
            **kwargs,
        )

    async def _send_message(self):
        # Generate field for yes and no options.
        _ = self.ctx.locale

        # NOTE: Name of the "Options" field in yes/no prompts.
        field_name = _("Options")

        # NOTE: Text for the "yes" option in a yes/no prompt.
        yes_text = _("{e:check} Respond with **yes** to confirm.")

        # NOTE: Text for the "no" option in a yes/no prompt.
        no_text = _("{e:cross} Respond with **no** to cancel.")

        field_value = self.bot.emotes.format(f"{yes_text}\n{no_text}")

        kwargs = self.kwargs.copy()
        fields = self.kwargs.get("fields", []).copy()
        fields.append(dict(name=field_name, value=field_value, inline=False))
        kwargs["fields"] = fields

        return await self.ctx.embed(**kwargs)

async def yesno(ctx, **kwargs):
    r"""
    Create and run a :class:`~senko.utils.io.YesNo` and return its result.

    Parameters
    ----------
    ctx: Union[senko.CommandContext, senko.PartialContext]
        The context under which to run the prompt.
    \*args
        Positional arguments to pass into :class:`~senko.utils.io.YesNo`.
    \*\*kwargs
        Keyword arguments to pass into :class:`~senko.utils.io.YesNo`.

    Raises
    ------
    InputTimeoutError
        Exception raised when the prompt times out.
    
    Returns
    -------
    Optional[bool]
        Either a boolean value denoting the user's choice, 
        or ``None`` if the prompt timed out.
    """
    prompt = YesNo(ctx, **kwargs)
    return await prompt.run()
