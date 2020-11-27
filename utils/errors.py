__all__ = ("QuietExit", "EmbedExit")


class QuietExit(Exception):
    """
    An exception that is silently ignored by its error handler added
    in :ref:`cogs_error_handlers`.

    The primary purpose of this class is to allow a command to be exited
    from within a nested call without having to propagate return values.
    """

    pass


class EmbedExit(Exception):
    r"""
    An exception that can be used to show a custom error message.

    The keyword arguments passed into the constructor of this
    exception are propagated into :func:`~senko.CommandContext.embed`
    by the error handler defined for this exception.

    See :func:`~cogs.error_handlers.handlers.handle_embed_exit`.

    Examples
    --------

    .. code-block:: python3

        # Somewhere inside a command.
        _ = ctx.locale

        raise EmbedExit(
            description=_("This is the embed description."),
            fields=[dict(name=_("It is fully localized."), value=_("How neat!"))]
        )

    Parameters
    ----------
    \*\*kwargs
        The same keyword arguments as accepted by
        :func:`~senko.CommandContext.embed`.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
