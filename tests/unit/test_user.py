import sqlalchemy as sa

import pytest

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from aiogram.types import User

from bot.utils import user_register
from bot.models import UserModel


pytestmark = pytest.mark.anyio

TEST_USER = User(
    id=1,
    is_bot=False,
    first_name='John',
    username='johnDoe',
    last_name='Doe',
    is_admin=True,
    email='johndoe@test.com'
)

async def test_user_register() -> None:
    result = await user_register(TEST_USER)

    assert result['user'].first_name == TEST_USER.first_name
    assert result['msg'] == 'Вы успешно зарегистрировались в системе.'


async def test_existing_user_register() -> None:
    result = await user_register(TEST_USER)

    assert result['msg'] == 'Вы уже зерегистрированы в системе.'
