from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram.types import User

from db import async_session

from schemas import UserBase
from models import UserModel

async def user_register(user: User) -> None:
    validated_user = UserBase(**user.model_dump())

    async with async_session.begin() as session:
        session.add(UserModel(**validated_user.model_dump(by_alias=True)))
