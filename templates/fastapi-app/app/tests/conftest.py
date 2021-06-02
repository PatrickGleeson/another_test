from httpx import AsyncClient
import pytest
from sqlalchemy_utils import create_database, drop_database

from app.database.base import Base
from app.database.session import database, engine
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def migrate():
    create_database(engine.url)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    drop_database(engine.url)


@pytest.fixture(scope="function")
async def delete_tables_data():
    async def __removing_table():
        for table in Base.metadata.tables:
            query = f"DELETE FROM {table}"
            await database.execute(query)

    await __removing_table()
    yield
    await __removing_table()


@pytest.fixture(autouse=True)
async def db():
    await database.connect()
    yield
    await database.disconnect()
