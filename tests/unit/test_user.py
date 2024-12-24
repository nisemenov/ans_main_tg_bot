import sqlalchemy as sa

import pytest

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload
from aiogram.types import User

from bot.utils import user_register
from core.models import UserModel
from tests.data_fixtures import TEST_USER


pytestmark = pytest.mark.anyio

async def test_user_register() -> None:
    result = await user_register(TEST_USER)

    assert result['user'].first_name == TEST_USER.first_name
    assert result['msg'] == 'Вы успешно зарегистрировались в системе.'


async def test_existing_user_not_register() -> None:
    result = await user_register(TEST_USER)

    assert result['msg'] == 'Вы уже зерегистрированы в системе.'
