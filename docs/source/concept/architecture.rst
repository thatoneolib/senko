.. _architecture:

Architecture
############

This page documents the architecture of the bot. This means the directory
structure, organization of packages and how modules are accessed internally.

The main goal behind the bot's architecture is to make as much of it reloadable
as possible. The central bot class and immediately related classes such as the
commands, cog and context classes are exempt from this.

Directories
***********

The following directories exist.

=========================== ====================================================
Path                        Description
=========================== ====================================================
``senko/``                  The core module of the bot. This is **not** reloadable.
``cogs/``                   Reloadable command modules.
``utils/``                  Reloadable shared utilities.
=========================== ====================================================

Reloading
*********

We differentiate between two types of reloading used to reload modules found in
the ``cogs`` directory and the ``utils`` directory respectively.

Cogs found in ``utils`` can be reloaded by calling the :meth:`~senko.Senko.reload_extension`
method of the bot using the extension that corresponds to the cog.

Utilities found in ``utils`` can instead be reloaded by calling :py:meth:`importlib.reload`
and passing the ``utils`` module. After reloading utilities, cogs that depend on
them should be reloaded as well to apply the changes. Please also note that
reloading ``utils`` does **not** update existing instances and will cause issues
with type comparisons between reloaded types.

Caveats
=======

One major caveat of reloading ``utils`` is that ``from``-imports
(e.g. ``from .xyz import XYZ``) in subpackages will not be reloaded and must
instead be manually reloaded.

So, instead of being able to simply call ``importlib.reload(utils)``, for some
subpackages, such as ``io`` we must instead use:

.. code-block:: python3

    importlib.reload(utils)
    importlib.reload(utils.io)
    importlib.reload(utils.io.input)
    # and so on...
