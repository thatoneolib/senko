__all__ = (
    "ELLIPSIS",
    "truncate",
)

ELLIPSIS = "…"
"""The ellipsis character used for :func:`utils.string.truncate`."""


def truncate(string, length):
    """
    Truncate a string to a given length.

    Functions as follows:

    * If length is 0 or less, returns an empty string.
    * If length is less than the length of the input string, returns the
      string truncated to length-1 and appends :data:`~utils.string.ELLIPSIS`.
    * Otherwise, returns the input string.

    Examples
    --------

    .. code-block:: python3

        description = "This is a very long and detailed description."
        shortened = utils.string.truncate(description, 20)
        # shortened = "This ia very long…"

    Parameters
    ----------
    string: str
        The string to truncate.
    length: int
        The maximum length of the string. Any characters past
        this limit will be removed and the last character is
        replaced with ``…``.

    Returns
    -------
    str
        The truncated string.
    """
    if length <= 0:
        return ""
    elif len(string) > length:
        return string[:length-1] + "…"
    else:
        return string

def human_join(items, bold=False, code=False, concatenator="and"):
    r"""
    Join a list of objects and return human readable representation.

    Examples
    --------

    .. code-block:: python3

        >>> from utils.string import human_join
        >>> human_join([])
        ""
        >>> human_join([1])
        "1"
        >>> human_join([1, 2])
        "1 and 2"
        >>> human_join([1, 2, 3])
        "1, 2 and 3"
        >>> human_join([1, 2, 3], concatenator="or")
        "1, 2 or 3"
        >>> human_join([1, 2], bold=True)
        "**1** and **2**"
        >>> human_join([1, 2], code=True)
        "`1` and `2`"

    Parameters
    ----------
    items: List[Union[Any]]]
        A list of strings or other objects to be joined.
    bold: Optional[bool]
        Whether to surround items with ``**``. Defaults to ``False``.
    code: Optional[bool]
        Whether to surround items with ``\`\```. Defaults to ``False``.
    concatenator: Optional[str]
        The concatenator to use for the second last and
        last item.
    
    Returns
    -------
    str
        The joined list of items.
    """
    fmt = "{}"
    if code:
        fmt = f"`{fmt}`"
    if bold:
        fmt = f"**{fmt}**"

    items = [fmt.format(item) for item in items]

    if len(items) == 0:
        return ""
    elif len(items) == 1:
        return str(items[0])
    
    return "{} {} {}".format(
        ", ".join(items[:-1]),
        concatenator,
        items[-1]
    )
