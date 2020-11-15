import pytest

# The database fixture uses senko.db_init, so we do not
# explicitly import it here.

@pytest.fixture
@pytest.mark.asyncio
async def connection(database):
    drop = """DROP TABLE IF EXISTS "test";"""
    create = """
    CREATE TABLE IF NOT EXISTS "test" (
        "data" JSONB NOT NULL
    );
    """
    async with database.acquire() as conn:
        await conn.execute(drop)
        await conn.execute(create)
        yield conn
        await conn.execute(drop)


@pytest.mark.db
@pytest.mark.asyncio
async def test_db_jsonb(connection):
    """Test custom JSONB encoding and decoding."""
    data = {"text": "Senko", "int": 123, "bool": True, "float": 1.5}

    insert = """INSERT INTO "test" ("data") VALUES ($1);"""
    select = """SELECT * FROM "test";"""

    await connection.execute(insert, data)
    row = await connection.fetchrow(select)

    fetched = row["data"]

    assert data["text"] == fetched["text"]
    assert data["int"] == fetched["int"]
    assert data["bool"] == fetched["bool"]
    assert data["float"] == fetched["float"]
