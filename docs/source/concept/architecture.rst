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

We can differentiate between two types of reloading used for the ``cogs`` and
``utils`` directory.

Cogs located in ``cogs`` can be reloaded using :meth:`.Senko.reload_extension`
with the name of the extension that corresponds to the cog.

Utilities from ``utils`` must instead be reloaded using :py:meth:`importlib.reload`.
After reloading utilities, cogs that depend on them should also be reloaded.
Please note that reloading ``utils`` does **not** update existing instances
of classes and may cause issues when comparing reloaded types.

Caveats
=======

One major caveat of reloading ``utils`` is that ``from``-imports in subpackages
(e.g. ``from .xyz import XYZ``) will not be reloaded. These must instead be
reloaded manually.

Thus instead of just calling ``importlib.reload(utils)`` we must repeat the
call for subpackages that use ``from``-imports internally´. This is the case
for the ``utils.io`` subpackage.

.. code-block:: python3

    # Reloads for packages that use from-imports must
    # be split up for the corresponding subpackages.

    importlib.reload(utils)
    importlib.reload(utils.io)
    importlib.reload(utils.io.input)
    # and so on...
