.. _utils_errors::

Errors
######

These exception types provide you with a quick and easy way of exiting a command
from any point with either a message or completely silenty. The functionality of
these exceptions is implemented in the handlers of the :ref:`cogs_error_handlers`
extension.


Quiet Exit
**********

An exception that allows you to silently exit a command from within nested
calls. 

Its error handler, :func:`~cogs.error_handlers.handlers.handle_quiet_exit`,
silently ignores the exception.

.. autoclass:: utils.errors.QuietExit

Embed Exit
**********

An exception that allows you to exit a command while displaying a custom error
message.

Its error handler, :func:`~cogs.error_handlers.handler.handle_embed_exit`,
uses the ``kwargs`` passed into the exception constructor to generate the
error message.

.. autoclass:: utils.errors.EmbedExit
