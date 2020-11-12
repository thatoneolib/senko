import gettext
import os

__all__ = ("Locale", "NullLocale")


class Locale(gettext.GNUTranslations):
    """
    A callable subclass of :py:class:`gettext.GNUTranslations`.

    Parameters
    ----------
    file: Union[str, os.PathLike]
        The path to the ``.mo`` file to load.

    Attributes
    ----------
    file: Union[str, os.PathLike]
        The ``.mo`` file this locale was created from.
    language: str
        The language of this locale.
    """

    def __init__(self, file):
        with open(file, "rb") as fp:
            super().__init__(fp)

        self.file = file
        self.language = self._info["language"]

    def __repr__(self):
        return f"<Locale file={self.file!r} language={self.language!r}>"

    def __call__(self, message):
        """
        Propagates the call to :meth:`~senko.Locale.gettext`.
        """
        return self.gettext(message)


class NullLocale(gettext.NullTranslations):
    """
    A callable subclass of :py:class:`gettext.NullTranslations`.

    Parameters
    ----------
    language: str
        The language ID to set.

    Attributes
    ----------
    file: None
        A placeholder attribute to match the interface of :class:`senko.Locale`.
        This is always ``None``.
    language: str
        The language of this locale.
    """

    def __init__(self, language):
        super().__init__()
        self.file = None
        self.language = language

    def __repr__(self):
        return f"<NullLocale file={self.file!r} language={self.language!r}>"

    def __call__(self, message):
        """
        Propagates the call to :meth:`~senko.NullLocale.gettext`.
        """
        return self.gettext(message)
