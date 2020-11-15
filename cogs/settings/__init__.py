from .cog import SettingsCog
from .errors import BadSetting, UnknownSetting
from .guild import GuildSettings


def setup(bot):
    bot.add_cog(SettingsCog(bot))
