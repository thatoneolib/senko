from .locale import Locale, NullLocale


class Locales:
    """
    A collection class for :class:`senko.Locale` objects.

    Parameters
    ----------
    default: Optional[str]
        The ID of the default locale that should be set as the fallback
        for all other locales.
    """

    def __init__(self, default=None):
        self.locales = dict()
        self._default = default
        self._fallback = NullLocale(language=self._default)

    @property
    def default(self):
        """
        Union[senko.Locale, senko.NullLocale]:
            The default locale. When the default locale is not
            available, this returns a :class:`senko.NullLocale`.
        """
        return self.locales.get(self._default, self._fallback)

    def load(self, file):
        """
        Load a locale from a ``.mo`` file.

        After a successful load the new locale will be available
        under a key equal to its :attr:`senko.Locale.language` attribute.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file path.
        """
        locale = Locale(file)

        # Set fallback if this is the default locale.
        if locale.language == self._default:
            for other in self.locales.values():
                other._fallback = locale
            locale._fallback = self._fallback
        else:
            locale._fallback = self.default

        self.locales[locale.language] = locale

    def unload(self, locale):
        """
        Unload a locale.

        Parameters
        ----------
        locale: str
            The ID of the locale to unload.

        Raises
        ------
        ValueError
            If the requested locale is not found.
        """
        if locale not in self.locales:
            raise ValueError(f"Unknown locale {locale!r}!")

        removed = self.locales.pop(locale)

        # Unset fallback if we unloaded the default locale.
        if removed.language == self._default:
            for other in self.locales.values():
                other._fallback = None

    def reload(self, locale):
        """
        Atomically reload a locale.

        Should reloading the locale fail then the previously
        loaded locale remains in place unmodified and the caught
        exception is raised.

        Parameters
        ----------
        locale: str
            The ID of the locale to reload.

        Raises
        ------
        ValueError
            If the requested locale is not found.
        """
        if locale not in self.locales:
            raise ValueError(f"Unknown locale {locale!r}!")

        # Unload the locale.
        backup = self.locales.pop(locale)
        if locale == self._default:
            for other in self.locales.values():
                other._fallback = None

        # Load the locale.
        try:
            self.load(backup.file)
        except:
            if locale == self._default:
                for other in self.locales.values():
                    other._fallback = backup

            self.locales[locale] = backup
            raise

    def has(self, locale):
        """
        Check whether a given locale is availab.e

        Parameters
        ----------
        locale: str
            The ID of the locale to check.

        Returns
        -------
        bool
            ``True`` when the locale is available, otherwise ``False``.
        """
        return locale in self.locales

    def get(self, locale):
        """
        Get a locale by its ID.

        If the requested locale does not exist the default
        locale is returned instead, which can either be a
        :class:`senko.Locale` or :class:`senko.NullLocale`.

        Parameters
        ----------
        locale: str
            The ID of the locale to get.

        Returns
        -------
        Union[senko.Locale, senko.NullLocale]
            A locale object. This can be the requested locale, a
            fallback locale or a :class:`senko.NullTranslations`.
        """
        try:
            return self.locales[locale]
        except KeyError:
            return self.default

    def get_all(self):
        """
        Get a list of all loaded locales.

        Returns
        -------
        List[senko.Locale]
            A list of locales.
        """
        return list(self.locales.values())

    def size(self):
        """
        Get the amount of loaded locales.
        """
        return len(self.locales)

    def __len__(self):
        return self.size()

    def __repr__(self):
        return f"<Locales default={self.default!r}>"
