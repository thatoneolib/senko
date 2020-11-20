class BadSetting(Exception):
    """
    Exception raised when an invalid value is provided
    for one or more settings when updating settings.
    """


class UnknownSetting(Exception):
    """
    Exception raised when attempting to access a setting
    that does not exist.
    """