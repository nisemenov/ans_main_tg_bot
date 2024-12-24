from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiogram.types import User

from core.models import UserModel, ServiceModel
from core.schemas import UserBase


TEST_USER = User(
    id=1,
    is_bot=False,
    first_name='John',
    username='johnDoe',
    last_name='Doe',
    is_admin=False,
    email='johndoe@test.com',
)

TEST_USER_WITH_SERVICE = UserBase(
    id=2,
    first_name='John2',
    username='johnDoe2',
    last_name='Doe2',
    is_admin=True,
    email='johndoe2@test.com',
)


async def user_instances(sessionmaker: async_sessionmaker[AsyncSession]) -> None:
    async with sessionmaker.begin() as session:
        user = UserModel(**TEST_USER_WITH_SERVICE.model_dump(by_alias=True))
        for s in ['wisdom', 'portal']:
            user.services.append(ServiceModel(title=s))
        session.add(user)
