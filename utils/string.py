import re
import inspect

__all__ = ("format_docstring", "human_join")

FMT_LIST   = r"^(\*|•|-) ((?:.)+)$((?:(?:\n^  )(?:.)+)*)"
FMT_BLOCK  = r"(^\| )((?:.)+)$((?:(?:\n^  )(?:.)+)*)"
FMT_LINE   = r"(?:(?<=^)|(?<=\n))(?:(?:.+)(?:\n|$))+"
FMT_IGNORE = "|".join(f"({fmt})" for fmt in (FMT_LIST, FMT_BLOCK))

RE_LIST   = re.compile(FMT_LIST, re.MULTILINE)
RE_BLOCK  = re.compile(FMT_BLOCK, re.MULTILINE)
RE_LINE   = re.compile(FMT_LINE, re.MULTILINE)
RE_IGNORE = re.compile(FMT_IGNORE, re.MULTILINE)

def _repl_line(match):
    return match.group(0).replace("\n", " ") + "\n"

def _repl_list(match):
    if match[3] == "":
        return "• " + match[2]
    else:
        return "• " + match[2] + match[3].replace("\n  ", " ")

def _repl_block(match):
    if match[3] == "":
        return match[2]
    else:
        return match[2] + match[3].replace("\n  ", " ")

def format_docstring(string):
    """
    Format a string using a rst-like formatting approach.

    Formats lines starting with ``*``, ``-`` and ``•`` followed by a
    space as bullet points. Subsequent lines starting with two spaces
    are appended to this line.

    Formats lines starting with ``|`` followed by a space as single lines,
    without appending normal text lines following it. Subsequent lines
    starting with two spaces are appended to this line.

    Finally, replaces linebreaks between not previously formatted lines
    of text with a space, collapsing them into a single line. Only lines
    of text separated by at least two linebreaks are not collapsed.
    
    Parameters
    ----------
    string: str
        The string to format.
    
    Returns
    -------
    str
        The formatted string.
    """
    string = inspect.cleandoc(string)

    # Find sections of text containing special formatting.
    sections = list()  # section : is special?
    position = 0
    for match in RE_IGNORE.finditer(string):
        start = match.start()
        end = match.end()

        if start != position:
            sections.append((string[position:start], 0))

        sections.append((string[start:end], 1))
        position = end

    if position != len(string):
        sections.append((string[position:len(string)], 0))

    # Apply formatting.
    builder = list()
    for section, is_special in sections:
        if section == "":
            continue
        if not is_special:
            section = RE_LINE.sub(_repl_line, section)
        elif RE_LIST.fullmatch(section) is not None:
            section = RE_LIST.sub(_repl_list, section)
        elif RE_BLOCK.fullmatch(section) is not None:
            section = RE_BLOCK.sub(_repl_block, section)

        builder.append(section)

    # Build and return.
    return "".join(builder).strip()

def human_join(iterable, concatenator="and", bold=False, code=False):
    """
    Join a list of items with commas and a concatenator.

    The final string enumerates the items found in the iterable
    in their string representation, using ``str(item)`` to format
    them.

    Examples
    --------

    .. code-block:: python3

        >>> from senko.utils import string
        >>> string.human_join([1])
        "1"
        >>> string.human_join([1, 2])
        "1 and 2"
        >>> string.human_join([1, 2, 3], "or")
        "1, 2 or 3"

    Parameters
    ----------
    iterable: List[Any]
        A non-empty iterable whose items should be enumerated.
    concatenator: Optional[str]
        An optional concatenator to use. Defaults to ``and``.
    code: Optional[bool]
        Whether items should be formatted in the markdown syntax
        for inline code-blocks. Defaults to ``False``.
    bold: Optional[bool]
        Whether items should be formatted in the markdown syntax
        for bold text. Defaults to ``False``.
    
    Raises
    ------
    ValueError
        If the iterable is empty.
    
    Returns
    -------
    str
        The formatted string.
    """
    fmt = "{}"
    if code:
        fmt = f"`{fmt}`"
    if bold:
        fmt = f"**{fmt}**"

    if len(iterable) == 0:
        raise ValueError("The iterable must not be empty!")

    if len(iterable) == 1:
        return fmt.format(str(iterable[0]))
    else:
        items = [fmt.format(str(item)) for item in iterable]

    return "{} {} {}".format(", ".join(items[:-1]), concatenator, items[-1])

