from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def check_db():
    if not database_exists(settings.SQLALCHEMY_CREATE_DATABASE_URI):
        create_database(settings.SQLALCHEMY_CREATE_DATABASE_URI)
