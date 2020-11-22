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
