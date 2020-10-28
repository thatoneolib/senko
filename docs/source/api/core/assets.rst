.. _core_assets:

Assets
######

To make working with images and emojis easier, Senko comes with a simple to use
and extend asset system. Based on the :class:`~senko.AssetLibrary` class, this
system allows for emojis and images to be stored in JSON-files
to be loaded by their respective libraries.

Instances of these libraries are accessible through :attr:`~senko.Senko.emotes`
(not ``emojis`` as that attribute is occupied by the emoji cache) and
:attr:`~senko.Senko.images` respectively.

Asset Library
=============

The base class for asset libraries is an abstract base class that declares the
shared interface among all asset library implementations.

.. autoclass:: senko.assets.AssetLibrary
    :members:

Emoji Library
=============

The emoji library creates :class:`discord.PartialEmoji` from JSON-files and
provides a handy formatting function to quickly replace template strings in a
given string with the corresponding emoji from the library.

The files loaded by this library must adhere to the following format:

.. code-block:: json

    {
        "discord_emoji":"<:senko:123456789012345678>",
        "unicode_emoji":"🦊"
    }

.. autoclass:: senko.Emojis
    :members:

Emoji Formatter
---------------

The custom string formatter that acts as the backbone of the
:meth:`senko.Emojis.format` method.

.. autoclass:: senko.assets.EmojiFormatter
    :members:

Image Library
=============

The image library loads image URLs from ``JSON``-structured files.

The files loaded by this library must adhere to the following format:

.. code-block:: json

    {
        "image":"https://senkobot.bitbucket.io/img/avatar.png",
    }

.. autoclass:: senko.Images
    :members: