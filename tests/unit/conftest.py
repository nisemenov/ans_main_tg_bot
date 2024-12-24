from __future__ import annotations

from typing import TYPE_CHECKING

from collections.abc import AsyncIterator

import pytest

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tests.data_fixtures import user_instances

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


pytestmark = pytest.mark.anyio


# filling DB with mocks
@pytest.fixture(scope='module', autouse=True)
async def fx_mock(
    sessionmaker: async_sessionmaker[AsyncSession]
) -> AsyncIterator[None]:
    
    await user_instances(sessionmaker)
    yield
