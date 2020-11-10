.. _utils_io:

IO Utilities
############

The ``senko.utils.io`` subpackage provides various utilities that simplify the
common use case of creating prompts or sending more advanced messages to users.

Input Prompt
************

Using the :class:`~senko.utils.io.Input` prompt you can create simple prompts
for additional user input in commands. The prompt supports converters just like
regular commands, so it is easy to use.

.. code-block:: python3

    import typing
    
    import senko
    from senko.utils import io
    from senko.converters import Int, Float

    @senko.command()
    async def pick(self, ctx):
        """Pick a number."""

        prompt = io.Input(
            ctx, 
            description="Pick a number.",
            converter=typing.Union[int, float],
            timeout=30.0,
            raise_errors=False,
            raise_timeout=False,
            delete_after=True
        )

        number = await prompt.run()

        if number is None:
            await ctx.send("You took too long to respond.")
        else:
            await ctx.send("You chose {number:,}.")

Class
=====

The actual class that implements the prompt.

.. autoclass:: senko.utils.io.Input
    :members:

Exceptions
==========

When ``raise_errors`` or ``raise_timeout`` are enabled, the :meth:`~.Input.run`
method may raise the following exceptions (except for :exc:`~.InputError`).

.. autoexception:: senko.utils.io.InputError

.. autoexception:: senko.utils.io.InputTimeoutError

.. autoexception:: senko.utils.io.InputStateError

.. autoexception:: senko.utils.io.InputConversionError
    :members:

.. autoexception:: senko.utils.io.InputUnionConversionError
    :members:

Shortcut
========

For ease of use, a shortcut function exists under :func:`senko.utils.io.input`.
A shortcut to quickly create a prompt exists under :meth:`senko.CommandContext.input`.

.. autofunction:: senko.utils.io.input

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

