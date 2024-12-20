from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import DeclarativeBase

from core.config import settings, SQLAlchemyConfig


class Base(DeclarativeBase):
    pass


sqlalchemy_config = SQLAlchemyConfig(
    connection_string=settings.SQLALCHEMY_DATABASE_URI,
)

async def check_db():
    if not database_exists(settings.SQLALCHEMY_CREATE_DATABASE_URI):
        create_database(settings.SQLALCHEMY_CREATE_DATABASE_URI)
