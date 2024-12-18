from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from pydantic import PostgresDsn


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

    def build_database_uri(self, path: str) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme='postgresql',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=path,
        )
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(self.build_database_uri(self.POSTGRES_DB))

    @computed_field
    @property
    def SQLALCHEMY_CREATE_DATABASE_URI(self) -> str:
        return str(self.build_database_uri('postgres'))


settings = Settings()
