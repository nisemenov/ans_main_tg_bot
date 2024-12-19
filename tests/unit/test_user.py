import sqlalchemy as sa

import pytest

from bot.utils import user_register
from schemas import UserBase

from models import UserModel

from db import async_session
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from aiogram.types import User

pytestmark = pytest.mark.anyio


user = User(
    id=1,
    is_bot=False,
    first_name='John',
    username='johnDoe',
    last_name='Doe',
    is_admin=True,
    email='johndoe@test.com'
)

async def test_user_register(sessionmaker: async_sessionmaker[AsyncSession]) -> None:
    await user_register(user)

    async with sessionmaker.begin() as session:
        result = await session.execute(sa.select(UserModel).filter_by(telegram_id=user.id))
        result: UserModel = result.scalar()

        assert result.first_name == user.first_name
