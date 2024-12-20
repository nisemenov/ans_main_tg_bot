from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, AsyncGenerator, Callable

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


if TYPE_CHECKING:
    from pydantic import PostgresDsn
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', env_ignore_empty=True, extra='ignore'
    )
    
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ''

    TOKEN: str

    def build_database_uri(self, scheme: str) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=scheme,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(self.build_database_uri('postgresql+asyncpg'))

    @computed_field
    @property
    def SQLALCHEMY_CREATE_DATABASE_URI(self) -> str:
        return str(self.build_database_uri('postgresql'))


settings = Settings()


@dataclass
class SQLAlchemyConfig:
    connection_string: str
    expire_on_commit: bool = False
    autoflush: bool = True
    create_engine: AsyncEngine = create_async_engine
    session_maker_class: async_sessionmaker[AsyncSession] = async_sessionmaker

    @property
    def get_engine(self) -> AsyncEngine:
        return self.create_engine(self.connection_string)
    
    @property
    def get_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return self.session_maker_class(
            bind=self.get_engine,
            expire_on_commit=self.expire_on_commit,
            autoflush=self.autoflush
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        session_maker = self.get_session_maker
        async with session_maker() as session:
            async with session.begin():
                yield session
