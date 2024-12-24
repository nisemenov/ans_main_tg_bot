from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import create_database, database_exists

from core.config import settings


async def check_db():
    if not database_exists(settings.SQLALCHEMY_CREATE_DATABASE_URI):
        create_database(settings.SQLALCHEMY_CREATE_DATABASE_URI)

            