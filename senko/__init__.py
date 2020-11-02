__title__       = "senko"
__author__      = "Maxee"
__license__     = "MIT"
__copyright__   = "Copyright 2020 Maxee"
__version__     = "1.0.0"

from .db import init_db
from .colour import Colour
from .assets import Emojis, Images
from .i18n import Locale, Locales, NullLocale
from . import utils

from .commands import CommandContext, PartialContext
from .bot import Senko
