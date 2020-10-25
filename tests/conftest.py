# Configuration file for pytest.
import os
import sys
import pytest

path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(path, "..")
sys.path.append(path)

from senko import init_db

# Database Fixture
@pytest.fixture(scope="function")
async def database(event_loop):
    """
    A fixture that passes passes an :class:`asyncpg.pool.Pool`.

    The connection to the database is made using the following credentials:

    ======= =========== =========== ======= ========
    User    Password    Host        Port    Database
    ======= =========== =========== ======= ========
    test    test        localhost   5432    test
    ======= =========== =========== ======= ========

    The ``test`` user must have full rights to the ``test`` database.
    """
    credentials = dict(
        user="test",
        password="test",
        host="localhost",
        port=5432,
        database="test"
    )

    pool = await init_db(**credentials)
    yield pool
    await pool.close()
