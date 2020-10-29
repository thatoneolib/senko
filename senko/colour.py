import discord

__all__ = ("Colour",)


class Colour(discord.Colour):
    """
    A subclass of :class:`discord.Colour` that represents a colour.
    """

    # red

    @classmethod
    def dark_red(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xbe1931``.
        """
        return cls(0xBE1931)

    @classmethod
    def red(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xdd2e44``.
        """
        return cls(0xDD2E44)

    # pink

    @classmethod
    def pink(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xe75a70``.
        """
        return cls(0xE75A70)

    @classmethod
    def light_pink(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xf4abba``.
        """
        return cls(0xF4ABBA)

    # purple

    @classmethod
    def dark_purple(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x744eaa``.
        """
        return cls(0x744EAA)

    @classmethod
    def purple(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x9266cc``.
        """
        return cls(0x9266CC)

    # blue

    @classmethod
    def dark_blue(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x2a6797``.
        """
        return cls(0x2A6797)

    @classmethod
    def blue(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x3b88c3``.
        """
        return cls(0x3B88C3)

    @classmethod
    def light_blue(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x5dadec``.
        """
        return cls(0x5DADEC)

    @classmethod
    def lighter_blue(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xbbddf5``.
        """
        return cls(0xBBDDF5)

    # green

    @classmethod
    def dark_green(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x3e721d``.
        """
        return cls(0x3E721D)

    @classmethod
    def green(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x77b255``.
        """
        return cls(0x77B255)

    @classmethod
    def light_green(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xa7d28b``.
        """
        return cls(0xA7D28B)

    # yellow

    @classmethod
    def yellow(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xfdcb58``.
        """
        return cls(0xFDCB58)

    @classmethod
    def light_yellow(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xfdd888``.
        """
        return cls(0xFDD888)

    # orange

    @classmethod
    def orange(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xf4900c``.
        """
        return cls(0xF4900C)

    @classmethod
    def light_orange(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xffac33``.
        """
        return cls(0xFFAC33)

    # brown

    @classmethod
    def dark_brown(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x662113``.
        """
        return cls(0x662113)

    @classmethod
    def brown(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xc1694f``.
        """
        return cls(0xC1694F)

    @classmethod
    def light_brown(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xd99e82``.
        """
        return cls(0xD99E82)

    # grey

    @classmethod
    def dark_grey(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x292f33``.
        """
        return cls(0x292F33)

    @classmethod
    def grey(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x66757f``.
        """
        return cls(0x66757F)

    @classmethod
    def light_grey(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x99aab5``.
        """
        return cls(0x99AAB5)

    @classmethod
    def lighter_grey(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xccd6dd``.
        """
        return cls(0xCCD6DD)

    # Custom colours

    @classmethod
    def white(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0xfffffe``.

        .. note::

            The colour code can not be ``0xffffff`` due to
            Discord displaying that colour as black.
        """
        return cls(0xFFFFFE)

    @classmethod
    def black(cls):
        """
        A factory method that returns a
        :class:`Colour` with a value of ``0x000000``.
        """
        return cls(0x000000)

    @classmethod
    def default(cls):
        """
        A factory method that returns
        a :class:`Colour` with a value of ``0xf39800``.
        """
        return cls(0xF39800)

    @classmethod
    def success(cls):
        """
        An alias for :meth:`senko.Colour.green`.
        """
        return cls.green()

    @classmethod
    def failure(cls):
        """
        An alias for :meth:`senko.Colour.red`.
        """
        return cls.red()

    @classmethod
    def error(cls):
        """
        An alias for :meth:`senko.Colour.dark_red`.
        """
        return cls.dark_red()

    @classmethod
    def hint(cls):
        """
        An alias for :meth:`senko.Colour.light_yellow`.
        """
        return cls.light_yellow()

    @classmethod
    def message(cls):
        """
        An alias for :meth:`senko.Colour.white`.
        """
        return cls.white()

    @classmethod
    def disabled(cls):
        """
        A factory method that returns the colour
        used for disabled embeds, a :class:`Colour`
        with a value of ``0x36393F``.
        """
        return cls(0x36393F)
