__title__       = "senko"
__author__      = "Maxee"
__license__     = "MIT"
__copyright__   = "Copyright 2020 Maxee"
__version__     = "1.0.0"

from .i18n import Locale, NullLocale, Locales
from .assets import Images, Emojis
from .colour import Colour
from .bot import Senko
from .db import init_db
from . import utils
