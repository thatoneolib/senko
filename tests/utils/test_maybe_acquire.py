import pytest
import utils

@pytest.mark.db
@pytest.mark.asyncio
async def test_without_connection(database):
    """Test maybe_acquire without an existing connection."""
    async with utils.db.maybe_acquire(database, None) as connection:
        value = await connection.fetchval("SELECT 1;")

    assert value == 1


@pytest.mark.db
@pytest.mark.asyncio
async def test_with_connection(database):
    """Test maybe_acquire with an existing connection."""
    async with database.acquire() as existing:
        async with utils.db.maybe_acquire(database, existing) as connection:
            value = await connection.fetchval("SELECT 1;")

    assert value == 1
