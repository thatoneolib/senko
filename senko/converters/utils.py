from discord.ext import commands


async def clean(ctx, argument):
    """
    Helper function that removes channel mentions and escapes markdown
    in the given ``argument`` string and returns the cleaned result.
    """
    converter = commands.clean_content(fix_channel_mentions=True, escape_markdown=True)
    return await converter.convert(ctx, argument)