.. _core_logging:

Logging
#######

The logging module is a central point for error handling and reporting. It
provides an interface to register exception handlers for command errors and
allows for log messages of certain logging domains to be sent through the
:data:`config.logging_webhook`.

The sole exception to this are messages sentusing the ``senko.logging`` domain.
Messages sent through this domain are explicitly filtered and not logged through
the webhook as to prevent recursive errors.

An instance of the logging module is available under :attr:`senko.Senko.logging`.

Adding Exception Handlers
*************************

Below you can find an example of how to add and remove an exception handler.
While this specific example is for a loadable extension, the function calls
are the same for any other use case.

Just keep in mind that when adding exception handlers for extensions, you need
to make sure that the handler is removed when the extension is unloaded.
Otherwise you will be left with ghost handlers that are never removed.

.. code-block:: python3

    class OutOfCoffeeError(Exception):
        """
        Exception raised when I am out of coffee.

        This should never be raised.
        """
        pass

    async def handle_out_of_coffee(ctx, exc):
        """
        Exception handler for :class:`~.OutOfCoffeeError`.
        """
        _ = ctx.locale
        await ctx.embed(
            title=_("Out of Coffee!"),
            description=_("It appears we have run out of coffee.")
        )

    def setup(bot):
        # Called when the extension is loaded.
        bot.logging.add_handler(OutOfCoffeeError, handle_out_of_coffee)
    
    def teardown(bot):
        # Called when the extension is unloaded.
        bot.logging.remove_handler(OutOfCoffeeError)
    
Configuring Logging Domains
***************************

Configuring logging domains is just as easy. Again, while this specific example
uses an extension, you can use these functions anywhere else.

.. important::

    You are advised to **not** enable logging for logging domains with frequent
    messages. When too many messages are sent in quick succession, the logging
    module will be ratelimited when attempting to send messages through the
    webhook. This may lead to errors.

.. code-block:: python3

    import logging

    LOG = logging.getLogger("shiro")

    def setup(bot):
        bot.logging.enable_logging("shiro", logging.WARNING)

        # The following are only logged to the console.
        LOG.debug("Hello there.")
        LOG.info("Hey, don't ignore me.")

         # The following is logged through the webhook.
        LOG.warning("HEY!")
    
    def teardown(bot):
        bot.logging.disable_logging("shiro")

Reference
*********

.. autoclass:: senko.Logging
    :members:
