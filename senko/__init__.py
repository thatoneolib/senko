__title__       = "senko"
__author__      = "Maxee"
__license__     = "MIT"
__copyright__   = "Copyright 2020 Maxee"
__version__     = "1.0.0"

# Utilities
from . import utils
from .db import init_db
from .colour import Colour

# Assets
from .assets import Emojis, Images
from .i18n import Locale, Locales, NullLocale, LocaleMixin

# Custom command framework
from . import converters
from .context import CommandContext, PartialContext
from .command import Command, Group, command, group
#from .cog import Cog, Category
from .bot import Senko
