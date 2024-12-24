from __future__ import annotations

import pytest

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from core.models import UserServiceAssociation


pytestmark = pytest.mark.anyio

async def test_service_through_user(sessionmaker: async_sessionmaker[AsyncSession]) -> None:
    async with sessionmaker.begin() as session:
        result = await session.execute(sa.select(UserServiceAssociation))
        
        assert len(result.all()) == 2
