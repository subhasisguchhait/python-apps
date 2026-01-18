import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from app.main import app
from app.core.database import get_db, Base
from tests.db_test import test_engine, get_test_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_test_database():
    """
    Create tables at start of test session and drop them at end.
    Ensures engine is disposed so no threads/connections keep pytest alive.
    """
    # Create schema
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Override app dependency: all routes using Depends(get_db) will use test DB
    app.dependency_overrides[get_db] = get_test_db

    yield

    # Cleanup schema
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Remove override (good hygiene)
    app.dependency_overrides.pop(get_db, None)

    # Close all connections / threads
    await test_engine.dispose()


@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
