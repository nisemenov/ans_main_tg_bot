from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from core.models import ServiceModel, NotificationModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.schemas import NotificationBase


async def create_notification(data: NotificationBase, session: AsyncSession):
    async with session as session:
        if service := await session.scalar(sa.select(ServiceModel).where(ServiceModel.title == data.service)):
            notification = NotificationModel(message=data.message, service=service)
            session.add(notification)
