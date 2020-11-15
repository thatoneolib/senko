def help_examples(*examples):
    """
    A decorator that adds help examples to a :class:`nyrm.Command` or
    :class:`nyrm.Group`.

    When displayed in the help page, examples will be formatted with
    the command prefix for the current context, replacing all found
    ``{prefix}`` templates with the command prefix.

    Example
    -------

    .. code-block:: python3

        @commands.command(name="hug", cls=nyrm.Command)
        @nyrm.help_examples("Use `{prefix}hug <user>` to give someone a warm hug.")
        async def hug(self, ctx, *, user:discord.User):
            # ...

    Parameters
    ----------
    *examples: str
        An argument list of strings to use as examples.
    """

    def pred(obj):
        try:
            obj.__help_examples__.extend(examples)
        except AttributeError:
            obj.__help_examples__ = list(examples)

        return obj

    return pred

def help_restrictions(*restrictions):
    """
    A decorator that adds a restrictions field to the help page of
    a :class:`nyrm.Command` or :class:`nyrm.Group`.

    Parameters
    ----------
    *restrictions: str
        An argument list of strings to use as restrictions.
    """

    def pred(obj):
        try:
            obj.__help_restrictions__.extend(restrictions)
        except AttributeError:
            obj.__help_restrictions__ = list(restrictions)

        return obj

    return pred

def help_icon(emoji):
    """
    A decorator that sets the emoji of the help page of a
    :class:`nyrm.Command`, :class:`nyrm.Group` or :class:`nyrm.Cog`.
    
    For subcommands without an icon, the icon of their parent
    command, if set, is displayed. This is recursive.

    Parameters
    ----------
    emoji: str
        The key of the emoji to get from :attr:`nyrm.Nyrm.emotes`.
    """

    def pred(obj):
        obj.__help_icon__ = emoji
        return obj

    return pred

def help_image(image):
    """
    A decorator that sets the image of the help page of a :class:`nyrm.Command`,
    :class:`nyrm.Group` or :class:`nyrm.Cog`.

    Parameters
    ----------
    image: str
        The key of the image to get from :attr:`nyrm.Nyrm.images`.
    """

    def pred(obj):
        obj.__help_image__ = image
        return obj

    return pred

def help_thumbnail(thumbnail):
    """
    A decorator that sets the thumbnail of the help page of a
    :class:`nyrm.Command`, :class:`nyrm.Group` or :class:`nyrm.Cog`.

    Parameters
    ----------
    thumbnail: str
        The key of the image to get from :attr:`nyrm.Nyrm.images`.
    """

    def pred(obj):
        obj.__help_thumbnail__ = thumbnail
        return obj

    return pred
