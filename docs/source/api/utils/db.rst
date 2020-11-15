.. _utils_db:

Database
########

Database utilities aim to make working with database connections easier.

Maybe Acquire
*************

The :class:`utils.db.maybe_acquire` class provides a convenient way to
dynamically acquire a database connection when required, or reuse an existing
connection.

.. autoclass:: utils.db.maybe_acquire

