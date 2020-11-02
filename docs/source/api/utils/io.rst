.. _utils_io:

IO Utilities
############

The ``senko.utils.io`` subpackage provides various utilities that simplify the
common use case of creating prompts or sending more advanced messages to users.

Embed Builder
*************

The embed builder utility provides a quick and easy way of building embeds
through a single function call rather than having to build them manually.

.. code-block:: python3

    @commands.command()
    async def avatar(self, ctx, *, user: discord.User):
        """Get someone's avatar."""

        embed = senko.utils.io.build_embed(
            title=f"{user.display_name}'s Avatar",
            description="What a magnificent being you are!",
            fields=[dict(name="URL", value=user.avatar_url)],
            image=user.avatar_url,
            footer=dict(text=str(ctx.author), icon_url=ctx.author.avatar_url),
            timestamp=datetime.now(tz=timezone.utc)
        )
        
        await ctx.send(embed=embed)

A shortcut for this function exists in :meth:`senko.CommandContext.embed`.

Reference
=========

.. autofunction:: senko.utils.io.build_embed

