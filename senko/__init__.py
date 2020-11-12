__title__       = "senko"
__author__      = "Maxee"
__license__     = "MIT"
__copyright__   = "Copyright 2020 Maxee"
__version__     = "1.0.0"

# Utilities
from .db import init_db
from .colour import Colour
from . import utils

# Assets
from .assets import Emojis, Images
from .l10n import Locale, Locales, NullLocale, LocaleMixin

# Custom command framework
from . import converters
from .context import CommandContext, PartialContext
from .command import Command, Group, command, group
from .cog import Cog
from .bot import Senko
