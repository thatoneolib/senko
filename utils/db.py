"""
maybe_acquire is based on source code written by Rapptz and licensed
under the MPL 2.0 (http://mozilla.org/MPL/2.0/).

Source: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/utils/db.py
"""


class maybe_acquire(object):
    """
    A helper class that can be used to maybe acquire a database
    connection, or reuse an existing one.

    Examples
    --------

    .. code-block:: python3

        # connection can be None or an already acquired database connection.

        async with utils.db.maybe_acquire(pool, connection) as conn:
            # Do something with the connection here. If the
            # connection was acquired for this context, it
            # is released afterwards.

    Parameters
    ----------
    pool: asyncpg.pool.Pool
        The database connection pool to fetch the connection from.
    connection: Optional[asyncpg.connection.Connection]
        An optional database connection to use. When no connection
        is passed, a new one is acquired from the database.
    """

    __slots__ = ("pool", "connection", "acquired")

    def __init__(self, pool, connection):
        self.pool = pool
        self.connection = connection
        self.acquired = False

    async def __aenter__(self):
        if self.connection is None:
            self.acquired = True
            self.connection = await self.pool.acquire()

        return self.connection

    async def __aexit__(self, *args):
        if self.acquired:
            await self.pool.release(self.connection)
