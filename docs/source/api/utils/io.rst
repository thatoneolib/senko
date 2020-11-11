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

For ease of use, you can use :func:`senko.utils.io.input` or 
:meth:`senko.CommandContext.input` to create an input prompt and
receive its result.

Example
=======

.. figure:: /_images/examples/utils/input.png
    :alt: An input prompt.

    An input prompt.

.. code-block:: python3

    prompt = senko.utils.io.Input(
        ctx,
        title=":1234: Enter a Number",
        description="Enter a number.",
        timeout=30.0,
        raise_errors=False,
        raise_timeout=False,
        delete_after=True
    )

    number = await prompt.run()

    if number is None:
        await ctx.send("You took too long to respond.")
    else:
        await ctx.send("Your number is {number:,}.")

Class
=====

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

.. autofunction:: senko.utils.io.input

Choice Prompt
*************

The choice prompt is a :class:`~.Input` that takes a dictionary or list of
options, prompts the context author to choose from them and returns the choice.

For ease of use, shortcuts to create a choice prompt and receive the result
exist under :func:`senko.utils.io.prompt` and :meth:`senko.CommandContext.choice`.

Example
=======

.. figure:: /_images/examples/utils/choice.png
    :alt: A choice prompt.

    A choice prompt.

.. code-block:: python3

    options = {
        ":apple: Apple":"apple",
        ":banana: Banana":"banana",
        ":kiwi: Kiwi":"kiwi",
    }

    # Alternatively, you could use a list of tuples.
    # options = [(":apple: Apple", "apple"), ...]

    prompt = senko.utils.io.Choice(
        ctx,
        options=options,
        allow_cancel=True,
        title=":writing_hand: Make a Choice",
        description="Pick a fruit you want to eat."
    )

    choice = await prompt.run()

    if choice is None:
        await ctx.send("You cancelled the prompt.")
    else:
        await ctx.send(f"You chose {choice}.")

The dictionary or list maps the displayed option to their associated value.
For example, ``{"first":1}`` would allow the user to choose "first".
When the option is chosen, the prompt would return 1.

Class
=====

.. autoclass:: senko.utils.io.Choice
    :members:
    
Exceptions
==========

.. autoexception:: senko.utils.io.ChoiceCancelledError

Shortcut
========

A shortcut function exists under :func:`senko.utils.io.choice`,
as well as :meth:`senko.CommandContext.choice`.

.. autofunction:: senko.utils.io.choice

Yes / No Prompt
***************

The choice prompt is a :class:`~.Input` that prompts the context author to
enter either yes or no, and returns an appropriate boolean value.

For ease of use, shortcuts to create a choice prompt and receive the result
exist under :func:`senko.utils.io.yesno` and :meth:`senko.CommandContext.yesno`.

Example
=======

.. figure:: /_images/examples/utils/yesno.png
    :alt: A yes / no prompt.

    A yes / no prompt.

.. code-block:: python3

    prompt = senko.utils.io.YesNo(
        ctx,
        title=":question: Touch fluffy tail?",
        description="Make your choice."
    )

    choice = await prompt.run()

    if choice:
        await ctx.send("*You touch the fluff.*")
    else:
        await ctx.send("*You resist the temptation.*")

Class
=====

.. autoclass:: senko.utils.io.YesNo
    :members:

Shortcut
========

A shortcut function exists under :func:`senko.utils.io.yesno`,
as well as :meth:`senko.CommandContext.yesno`.

.. autofunction:: senko.utils.io.yesno

Embed Builder
*************

The embed builder utility provides a quick and easy way of building embeds
through a single function call rather than having to build them manually.

.. code-block:: python3

    @senko.command()
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
