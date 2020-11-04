.. _core_cog:

Cog
###

As with the custom command implementations, the modified cog implementation
available under :class:`senko.Cog` provides some additional properties for
localization and new attributes that are useful for organizing commands into
categories without having to define them in the same cog.

Class Parameters
****************

Similar to the ``name`` class parameter, :class:`senko.Cog` accepts two new
class parameters: ``category`` and ``hidden``.

When set, the ``category`` parameter defines under which cog the commands of
a new cog should be listed in the help command.

.. code-block:: python3

    class HelpCommand(senko.Cog, category="meta"):
        """
        This cog is never visible in the help command.

        Its only command shows up under the meta cog instead.
        """
        @senko.command()
        async def help(self, ctx, *, term:str=None):
            # ...
    
    class Meta(senko.Cog, name="meta"):
        """
        Helpful meta commands.
        """
        # Despite having no commands, the help command is
        # listed as being part of this cog in the help command.

The ``hidden`` parameter sets the ``hidden`` attribute of all commands
added to the cog to ``hidden``. It also prevents the cog from being listed
in the help command.

Cog
***

.. autoclass:: senko.Cog
    :members:

Cog Overrides
*************

:class:`senko.cog.overrides.CogOverrides` is a metaclass that is used to create
:class:`senko.Cog`. 

You should not need to use this. It is only documented for completion.

.. autoclass:: senko.cog.overrides.CogOverrides
    :members: