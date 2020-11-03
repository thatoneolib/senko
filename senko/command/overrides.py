import asyncio
import datetime
import functools

import discord
import senko
from discord.ext import commands

# Stop pylint from sprinkling errors everywhere.
# pylint: disable=no-member


class CommandOverrides:
    """
    A mixin that implements various overrides for commands.

    When combined with a :class:`discord.ext.commands.Command` or
    :class:`discord.ext.commands.Group` subclass, this class injects
    various overrides that enable the custom behavior utilized by the bot.

    This class adds the following overrides:

    * The ``_actual_conversion`` method injects our own type converters.
    * Adds various getter methods for properties with localization support.
    """

    async def _actual_conversion(self, ctx, converter, argument, param):
        """
        The custom parameter conversion method.

        This method injects the custom converters found in ``senko.converters``.

        In addition, it sets the ``param`` attribute for raised
        :class:`~discord.ext.commands.BadArgument` exceptions.
        """
        if converter is bool:
            converter = senko.converters.Bool
        elif converter is int:
            converter = senko.converters.Int
        elif converter is float:
            converter = senko.converters.Float

        try:
            module = converter.__module__
            if module.startswith("discord.") and not module.endswith("converter"):
                converter_name = converter.__name__
                converter = getattr(senko.converters, converter_name, converter)
        except AttributeError:
            pass

        try:
            return await super()._actual_conversion(ctx, converter, argument, param)
        except commands.BadArgument as exc:
            exc.param = param
            raise

    @discord.utils.cached_property
    def locale_id(self):
        """
        The base ID for translatable messages related to a command.

        This ID, when combined with a valid suffix, can be used to
        look up translated attributes of a command.

        Format: ``#command_<qualified_name>``.

        Examples
        --------

        ======================= ================================================
        Qualified Name          Locale ID
        ======================= ================================================
        ``parent``              ``#command_parent``
        ``parent child``        ``#command_parent_child``
        ======================= ================================================

        For example, to look up the localized name of a given
        command, you would use ``#command_<qualified_name>`_name``.

        Returns
        -------
        str
            The message ID as described.
        """

        key = self.qualified_name.replace(" ", "_")
        return f"#command_{key}"

    @property
    def signature(self):
        """
        str: Returns a POSIX-like signature useful for help command output.

        To get a localized version of the signature, use
        :meth:`~senko.Command.get_signature` instead.
        """
        return self.get_signature()

    def get_signature(self, locale=None):
        """
        Get the signature for the command.

        Parameters
        ----------
        locale: Optional[senko.Locale]
            The locale translate the signature with.

        Returns
        -------
        str
            The command signature.
        """
        # This method is a reimplementation of the original signature property.
        # You can find the definition in discord/ext/commands/core.py.

        # Prefer usage over generated signature.
        if self.usage is not None:
            return self.get_usage(locale=locale)

        # Generate signature string.
        builder = list()
        params = self.clean_params
        if not params:
            return ""

        for name, param in params.items():
            if locale is not None:
                # Format: #command_<command>_parameter_<name>
                name = locale(f"{self.locale_id}_parameter_{name}")

            # Display optional parameters as [optional] or [optional=default].
            if param.default is not param.empty:
                show_value = (
                    param.default
                    if isinstance(param.default, str)
                    else param.default is not None
                )

                if show_value:
                    builder.append(f"[{name}={param.default}]")
                else:
                    builder.append(f"[{name}]")

            # Display positional optional parameters as [optional...].
            elif param.kind == param.VAR_POSITIONAL:
                if self.require_var_positional:
                    builder.append(f"<{name}...>")
                else:
                    builder.append(f"[{name}...]")

            # Display keyword only parameters as <required...>.
            elif param.kind == param.KEYWORD_ONLY:
                builder.append(f"<{name}...>")

            # Display all other parameters as <required>.
            else:
                builder.append(f"<{name}>")

        return " ".join(builder)

    def get_name(self, locale=None):
        """
        Get the name of this command.

        Parameters
        ----------
        locale: Optional[senko.Locale]
            An optional locale to localize the name with.

        Returns
        -------
        str
            The command name or the localized command name.
        """
        if locale is None:
            return self.name
        else:
            return locale(f"{self.locale_id}_name")

    def get_qualified_name(self, locale=None):
        """
        Get the qualified name of the command.

        Parameters
        ----------
        locale: Optional[senko.Locale]
            An optional locale to localize the name with.

        Returns
        -------
        str
            The qualified name of the command.
        """
        if locale is None:
            return self.qualified_name

        entries = []
        command = self
        entries.append(self.get_name(locale))

        while command.parent is not None:
            command = command.parent
            entries.append(command.get_name(locale))

        return " ".join(reversed(entries))

    def get_help(self, locale=None):
        """
        Get the long help text of the command.

        Parameters
        ----------
        locale: senko.Locale
            An optional locale to localize the string with.

        Returns
        -------
        Optional[str]
            The long help text of the command or ``None`` if
            the command does not have a long help text.
        """
        if self.help is None:
            return None

        if locale is not None:
            return locale(f"{self.locale_id}_help")
        else:
            return self.help

    def get_brief(self, locale=None):
        """
        Get the brief help text of the command.

        Parameters
        ----------
        locale: senko.Locale
            An optional locale to localize the string with.

        Returns
        -------
        Optional[str]
            The brief help text of the command or ``None`` if
            the command does not have a brief help text.
        """
        if self.brief is None:
            return None

        if locale is not None:
            return locale(f"{self.locale_id}_brief")
        else:
            return self.brief

    def get_short_doc(self, locale=None):
        """
        Get the short documentation of the command.

        By default, this is the same as :meth:`senko.Command.get_brief`.
        If that lookup returns ``None``, the first line of the result of
        :meth:`senko.Command.get_help` is returned instead. The ``locale``
        parameter is passed to these calls if it is set.

        Parameters
        ----------
        locale: senko.Locale
            An optional locale to localize the string with.

        Returns
        -------
        Optional[str]
            The brief help text of the command or ``None`` if
            the command does not have a brief help text.
        """
        if self.brief is not None:
            return self.get_brief(locale=locale)

        if self.help is not None:
            string = self.get_help(locale=locale)
            return string.split("\n", 1)[0]

        return None

    def get_usage(self, locale=None):
        """
        Get a replacement for arguments in the default help text.

        Parameters
        ----------
        locale: senko.Locale
            An optional locale to localize the string with.

        Returns
        -------
        Optional[str]
            The usage string or ``None`` if the command does
            not have a usage string.
        """
        if self.usage is None:
            return None

        if locale is None:
            return self.usage

        # Format: #command_<qualified_name>_usage
        return locale(f"{self.locale_id}_usage")

    def get_description(self, locale=None):
        """
        Get the description of this command.

        Parameters
        ----------
        locale: senko.Locale
            An optional locale to localize the aliases with.

        Returns
        -------
        Optional[str]
            The description or localized description, or
            ``None`` if no description was set for this command.
        """
        if self.description is None:
            return None

        if locale is None:
            return self.description

        # Format: #command_<qualified_name>_description
        return locale(f"{self.locale_id}_description")

    def get_aliases(self, locale=None):
        """
        Get the list of aliases the command can be invoked under.

        Parameters
        ----------
        locale: senko.Locale
            An optional locale to localize the aliases with.

        Returns
        -------
        List[str]
            A list of aliases or localized aliases. The list may be empty.
        """
        if locale is None:
            return self.aliases

        aliases = []
        for alias in self.aliases:
            # Format: #command_<qualified_name>_alias_<alias>
            aliases.append(locale(f"{self.locale_id}_alias_{alias}"))

        return aliases
