import logging

import senko
from senko.utils import CaseInsensitiveDict


class LocaleMixin:
    """
    A mixin for :class:`discord.ext.commands.Groupmixin`-derived
    classes that adds support for getting commands by their localized
    names using the :attr:`senko.CommandContext.locale` property.

    The main purpose of this class is to override the ``get_command``
    method with one that allows a :class:`senko.Locale` to be passed in
    to allow commands to be looked up using their localized names.

    For this purpose, this class internally maintains a cache of localized
    names for the commands added to it. This cache is updated whenever
    a locale is added or removed by the locale source, or a command is added
    or removed to the mixin instance.
    """

    def __init__(self, *args, **kwargs):
        self._locale_source = None

        # The locale map is a dictionary that maps the IDs of locales
        # available through the configured locale source to command name
        # dictionaries.
        # Such a dictionary maps the names and aliases of commands added
        # to the LocaleMixin, localized using the corresponding locale,
        # to the corresponding command.
        # This allows for an efficient lookup for localized names in invoke
        # and reinvoke.

        if kwargs.get("case_insensitive", True):
            self._locale_map = CaseInsensitiveDict()
        else:
            self._locale_map = dict()

        super().__init__(*args, **kwargs)

    def set_locale_source(self, source=None):
        """
        Set the locale source to use for name resolution.

        This causes the existing command name cache to be regenerated.

        Parameters
        ----------
        source: Optional[senko.Locales]
            The locale source to use. Can be set to ``None`` to
            remove a previously configure locale source.
        """
        # Unregister a previously configure locale source and clear the map.
        if self._locale_source is not None:
            self._locale_source.remove_mixin(self)
            self._locale_map.clear()

        if source is None:
            return

        # Set the locale source, which subsequently regenerates the cache.
        self._locale_source = source
        self._locale_source.add_mixin(self)
        for locale in self._locale_source.get_all():
            self._add_locale(locale)

    def _new_map(self):
        """
        Union[senko.utils.CaseInsensitiveDict, dict]: Get a new blank mapping.
        The type depends on whether the mixin is ``case_insensitive`` or not.
        """
        return CaseInsensitiveDict() if self.case_insensitive else dict()

    def _add_locale(self, locale):
        """
        Add a locale.
        """
        for command in self.commands:
            self._add_command_map_for_locale(command, locale)

    def _remove_locale(self, locale):
        """
        Remove a locale.
        """
        self._locale_map.pop(locale.language, None)

    def _add_command_map_for_locale(self, command, locale):
        """
        Generate the localization mapping for a command.
        """
        mapping = self._new_map()

        mapping[locale(f"{command.locale_id}_name")] = command
        for alias in command.aliases:
            mapping[locale(f"{command.locale_id}_alias_{alias}")] = command

        try:
            locale_mapping = self._locale_map[locale.language]
        except KeyError:
            locale_mapping = self._locale_map[locale.language] = self._new_map()

        # Add the new keys one by one and check for duplicates.
        for key, value in mapping.items():
            if key in locale_mapping:
                logger = logging.getLogger("senko.i18n")
                original = mapping[key]
                conflict = value

                logger.warning(
                    f"Duplicate {locale.language!r} translation for "
                    f"commands {original!r} and {conflict!r} : {key!r}. "
                    f"Skipping adding translation for {conflict!r}.!"
                )

                continue
            else:
                locale_mapping[key] = value

    def _remove_command_map_for_locale(self, command, locale):
        """
        Remove the localization mapping for a command.
        """
        try:
            locale_mapping = self._locale_map[locale.language]
        except KeyError:
            return

        for key, value in list(locale_mapping.items()):
            if value is command:
                locale_mapping.pop(key)

    def add_command(self, command):
        """
        Add a command to this object.

        This automatically sets up locale mappings for the command.

        Parameters
        ----------
        command: Union[senko.Command, senko.Group]
            The command to add.

        Raises
        ------
        TypeError
            When the passed command is not a :class:`senko.Command`
            or :class:`senko.Group`.
        """
        if not isinstance(command, (senko.Command, senko.Group)):
            t = type(command).__name__
            raise TypeError(f"command must be senko.Command or senko.Group, not {t!r}!")
        
        super().add_command(command)

        if self._locale_source is not None:
            for locale in self._locale_source.get_all():
                self._add_command_map_for_locale(command, locale)

            if isinstance(command, LocaleMixin):
                command.set_locale_source(self._locale_source)

    def remove_command(self, command):
        """
        Remove a command from this object.

        This clears the corresponding localization mappings.

        Parameters
        ----------
        command: str
            The name of the command to remove.

        Raises
        ------
        TypeError
            When the passed command is not a :class:`senko.Command`
            or :class:`senko.Group`.
        """
        removed = super().remove_command(command)

        if self._locale_source is not None:
            for locale in self._locale_source.get_all():
                self._remove_command_map_for_locale(removed, locale)

        return removed

    def get_command(self, name, *, locale=None):
        """
        Get a command from the internal list of commands.

        Parameters
        ----------
        name: str
            The name of the command to get.
        locale: Optional[senko.Locale]
            An optional locale to consult when resolving the command.
            If no command is found using the locale, the default command
            names are used as a fallback.

        Returns
        -------
        Optional[Union[senko.Command, senko.Group]]
            The requested command, or ``None`` if no command was found.
        """
        if name is None:
            return None

        # Resolve direct children using their name.
        if not " " in name:
            if locale:
                mapping = self._locale_map.get(locale.language, dict())
                return mapping.get(name, self.all_commands.get(name))
            else:
                return self.all_commands.get(name)

        # Otherwise resolve subcommands.
        names = name.split()
        if not names:
            return None

        command = self.get_command(names[0], locale=locale)
        if not isinstance(command, senko.Group):
            return command

        # If the command is a group, walk the command tree.
        for name in names[1:]:
            try:
                command = command.get_command(name, locale=locale)
            except (AttributeError, KeyError):
                return None

        return command
