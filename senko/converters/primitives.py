from babel.core import UnknownLocaleError
from babel.numbers import NumberFormatError, parse_decimal, parse_number

from discord.ext import commands

from .utils import clean

__all__ = ("Int", "Float", "Bool")


class Int(commands.Converter):
    """
    Converts to :class:`int`.

    Parameters
    ----------
    min: Optional[int]
        When set, the passed number must be greater than or equal to ``max``.
    max: Optional[int]
        When set, the passed number must be less than or equal to ``max``.
    """

    def __init__(self, min=None, max=None):
        self._min = min
        self._max = max
        super().__init__()

    def _parse(self, ctx, argument):
        # Attempt to parse using babel.numbers.parse_number first.
        # This handles special cases such as thousands separators.
        try:
            return parse_number(argument, locale=ctx.locale.language)
        except (UnknownLocaleError, NumberFormatError):
            pass

        try:
            return int(argument)
        except (ValueError, TypeError):
            pass

        return None

    async def convert(self, ctx, argument):
        number = self._parse(ctx, argument)

        if number is None:
            _ = ctx.locale
            # NOTE: Error message for the integer converter.
            message = _("Could not interpret `{}` as an integer.")
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned))

        elif self._min is not None and number < self._min:
            _ = ctx.locale
            # NOTE: Error message for the integer converter.
            message = _("The number is too small. It should be at least {}.")
            raise commands.BadArgument(message.format(self._max))

        elif self._max is not None and number > self._max:
            _ = ctx.locale
            # NOTE: Error message for the integer converter.
            message = _("The number is too big. It should be at most {}.")
            raise commands.BadArgument(message.format(self._max))

        else:
            return number


class Float(commands.Converter):
    """
    Converts to :class:`float`.

    Parameters
    ----------
    min: Optional[float]
        When set, the passed number must be greater than or equal to ``max``.
    max: Optional[float]
        When set, the passed number must be less than or equal to ``max``.
    """

    def __init__(self, min=None, max=None):
        self._min = min
        self._max = max

    def _parse(self, ctx, argument):
        # Attempt to parse using babel.numbers.parse_number first.
        # This handles special cases such as thousands separators.
        try:
            return parse_decimal(argument, locale=ctx.locale.language)
        except (UnknownLocaleError, NumberFormatError):
            pass

        try:
            return float(argument)
        except (ValueError, TypeError):
            pass

        return None

    async def convert(self, ctx, argument):
        number = self._parse(ctx, argument)

        if number is None:
            _ = ctx.locale
            # NOTE: Error message for the float converter.
            message = _("Could not interpret `{}` as a decimal number.")
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned))

        elif self._min and number < self._min:
            _ = ctx.locale
            # NOTE: Error message for the float converter.
            message = _("The number is too small. It should be at least {}.")
            raise commands.BadArgument(message.format(self._max))

        elif self._max and number > self._max:
            _ = ctx.locale
            # NOTE: Error message for the float converter.
            message = _("The number is too big. It should be at most {}.")
            raise commands.BadArgument(message.format(self._max))

        else:
            return number


class Bool(commands.Converter):
    """
    Converts to :class:`bool`.

    Accepts both ``true``, ``false`` and a few different equivalent
    words, such as ``yes`` and ``no``. Acceptes both unlocalized and
    localized variants.

    | Accepted values for ``True``: ``true``, ``yes``, ``y``
    | Accepted values for ``False``: ``false``, ``no``, ``n``
    """

    async def convert(self, ctx, argument):
        _ = ctx.locale
        folded = argument.casefold()

        true = [
            "true",
            "yes",
            "y",
            # NOTE: Value for the boolean converter. Word for "true".
            # DEFAULT: true
            _("#converter_bool_true"),
            # NOTE: Value for the boolean converter. Word for "yes".
            # DEFAULT: yes
            _("#converter_bool_yes"),
            # NOTE: Value for the boolean converter. First letter of "yes".
            # DEFAULT: y
            _("#converter_bool_y"),
        ]

        false = [
            "false",
            "no",
            "n",
            # NOTE: Value for the boolean converter. Word for "false".
            # DEFAULT: false
            _("#converter_bool_false"),
            # NOTE: Value for the boolean converter. Word for "no".
            # DEFAULT: no
            _("#converter_bool_no"),
            # NOTE: Value for the boolean converter. First letter of "no".
            # DEFAULT: n
            _("#converter_bool_n"),
        ]

        if folded in true:
            return True

        elif folded in false:
            return False

        else:
            # NOTE: Error message for the boolean converter.
            message = _("`{}` could not be interpreted as yes or no.")
            cleaned = await clean(ctx, argument)
            raise commands.BadArgument(message.format(cleaned))
