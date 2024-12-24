from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from core.config import sqlalchemy_config as config

from core.schemas import UserBase
from core.models import UserModel

if TYPE_CHECKING:
    from aiogram.types import User


async def user_register(user: User) -> dict:
    validated_user = UserBase(**user.model_dump())

    try:
        async with config.get_session() as session:
            session.add(UserModel(**validated_user.model_dump(by_alias=True)))
        return {
            'user': validated_user,
            'msg': 'Вы успешно зарегистрировались в системе.'
        }
    except IntegrityError:
        return {
            'user': validated_user,
            'msg': 'Вы уже зерегистрированы в системе.'
        }
