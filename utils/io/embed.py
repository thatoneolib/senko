import discord
import senko

__all__ = ("build_embed",)

EMPTY = discord.Embed.Empty


def build_embed(**kwargs):
    """
    Build a :class:`discord.Embed` from keyword arguments.

    Parameters
    ----------
    title: Optional[str]
        The embed title.
    description: Optional[str]
        The embed description.
    url: Optional[str]
        The embed url.
    colour: Optional[Union[discord.Colour, int]]
        The embed colour. Set to ``None`` to create an embed without a colour.
        Defaults to :meth:`senko.Colour.default`.
    timestamp: datetime.datetime
        The embed timestamp.
    thumbnail: str
        The embed thumbnail.
    image: str
        The embed image.
    author: Union[str, dict]
        The embed author. When set to a string, this is used as the author name.
        When set to a dict, this is passed into :meth:`discord.Embed.set_author`.
    footer: Union[str, dict]
        The embed footer. When set to a string, this is used as the footer text.
        When set to a dict, this is passed into :meth:`discord.Embed.set_footer`.
    fields: List[dict]
        An iterable of dictionaries to pass into :meth:`discord.Embed.add_field`.

    Returns
    -------
    discord.Embed
        An embed constructed from the provided parameters.
    """
    embed = discord.Embed()
    embed.title = kwargs.get("title", EMPTY)
    embed.description = kwargs.get("description", EMPTY)
    embed.timestamp = kwargs.get("timestamp", EMPTY)
    embed.url = kwargs.get("url", EMPTY)
    embed.set_image(url=kwargs.get("image", EMPTY))
    embed.set_thumbnail(url=kwargs.get("thumbnail", EMPTY))

    colour = kwargs.get("colour", senko.Colour.default())
    if colour is not None:
        embed.colour = colour

    author = kwargs.get("author", EMPTY)
    if isinstance(author, dict):
        embed.set_author(
            name=author["name"],
            url=author.get("url", EMPTY),
            icon_url=author.get("icon_url", EMPTY),
        )
    elif isinstance(author, str):
        embed.set_author(name=author)

    footer = kwargs.pop("footer", EMPTY)
    if isinstance(footer, dict):
        embed.set_footer(
            text=footer.get("text", EMPTY),
            icon_url=footer.get("icon_url", EMPTY)
        )
    elif isinstance(author, str):
        embed.set_footer(text=footer)

    for field in kwargs.pop("fields", []):
        embed.add_field(
            name=field["name"],
            value=field["value"],
            inline=field.get("inline", True)
        )

    return embed
