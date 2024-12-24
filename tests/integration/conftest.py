from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from httpx import AsyncClient, ASGITransport

from api.app import app

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


pytestmark = pytest.mark.anyio


@pytest.fixture(name='client')
async def fx_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://testserver'
    ) as client:
        yield client
