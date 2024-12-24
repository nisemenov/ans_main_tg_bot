from __future__ import annotations

from typing import TYPE_CHECKING

from collections.abc import AsyncIterator

import pytest

from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from core.config import sqlalchemy_config as config
from core.config import Settings
from core.models import Base

from .data_fixtures import user_instances

if TYPE_CHECKING:
    from typing import AsyncGenerator
    from pydantic import PostgresDsn
    from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine


pytestmark = pytest.mark.anyio


# for connection string URI
class TestSettings(Settings):
    def build_database_uri(self, scheme: str) -> PostgresDsn:
        from pydantic_core import MultiHostUrl
        
        return MultiHostUrl.build(
            scheme=scheme,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path='test_ans_main_tg_bot',
        )


test_settings = TestSettings()


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session', autouse=True)
async def fx_db() -> AsyncGenerator[None]:

    if not database_exists(test_settings.SQLALCHEMY_CREATE_DATABASE_URI):
        create_database(test_settings.SQLALCHEMY_CREATE_DATABASE_URI)
    yield

    drop_database(str(test_settings.SQLALCHEMY_CREATE_DATABASE_URI))


@pytest.fixture(name='engine', scope='module')
async def fx_engine() -> AsyncEngine:
    return create_async_engine(
        url=test_settings.SQLALCHEMY_DATABASE_URI,
        poolclass=NullPool,
    )


@pytest.fixture(name='sessionmaker', scope='module')
def fx_session_maker_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False)


# changing DB string
@pytest.fixture(autouse=True)
async def fx_sqlalchemy_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        config, 
        'connection_string', 
        test_settings.SQLALCHEMY_DATABASE_URI
    )


# drop/create DB meta with mocks
@pytest.fixture(scope='module', autouse=True)
async def fx_drop_create_meta(engine: AsyncEngine) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


# filling DB with mocks
@pytest.fixture(scope='module', autouse=True)
async def fx_mock(
    sessionmaker: async_sessionmaker[AsyncSession]
) -> AsyncIterator[None]:
    
    await user_instances(sessionmaker)
    yield
