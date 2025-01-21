import pytest
from .shared import prepare_demodata, prepare_in_memory_sqllite

@pytest.mark.asyncio
async def test_table_users_feed():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    # data = get_demodata()

def test_connection_string():
    from src.DBDefinitions import ComposeConnectionString
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString


def test_connection_uuidcolumn():
    from src.DBDefinitions import UUIDColumn
    from sqlalchemy.orm import DeclarativeBase

    class TestBase(DeclarativeBase):
        pass

    # Mock model for testing
    class MockModel(TestBase):
        __tablename__ = "mock_table"
        id = UUIDColumn()

    # Verify that the id column was correctly configured
    column = MockModel.__table__.columns.get("id")
    assert column is not None, "id column was not created"
    assert column.comment == "primary key"
    assert column.primary_key, "id column is not a primary key"
    assert column.index, "id column is not indexed"



@pytest.mark.asyncio
async def test_table_start_engine():
    from src.DBDefinitions import startEngine
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
